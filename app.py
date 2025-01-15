from flask import Flask, jsonify, request
import requests
import base64
import json

app = Flask(__name__)

# Configurações
credentials = {
    "client_id": "",
    "client_secret": "",
}

certificado = './certificado.pem'  # Caminho do certificado PEM, lembre-se de converter o certificado P12 para o formato PEM (Caso não saiba como converter, consulte o README)

# ---------------------------------------------- URL'S BASE ----------------------------------------------

# url de Homologação
"""
    Deixe a variável abaixo descomentada para usar a url de Homologação (testes)
"""
PIX_API_BASE = "https://pix-h.api.efipay.com.br" 

# url de Produção
"""
    Deixe a variável abaixo descomentada para usar a url de Produção
"""
# PIX_API_BASE = "https://pix.api.efipay.com.br" 

# ---------------------------------------------- Autenticação ----------------------------------------------

auth = base64.b64encode(
    (f"{credentials['client_id']}:{credentials['client_secret']}").encode()
).decode()

def get_access_token():
    """
    Obtém todos os dados da resposta do servidor PIX.
    """
    token_url = f"{PIX_API_BASE}/oauth/token"
    payload = {
        "grant_type": "client_credentials"
    }
    headers = {
        'Authorization': f"Basic {auth}",
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(token_url, json=payload, cert=certificado, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao obter o token de acesso: {str(e)}")

@app.route('/auth', methods=['GET'])
def authenticate():
    """
    Endpoint para autenticação e obtenção de token.
    """
    try:
        token_data = get_access_token()
        return jsonify({"access_token": token_data['access_token']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------- ENDPOINTS DE PIX IMEDIATO ----------------------------------------------

@app.route('/pix/charge', methods=['POST'])
def create_pix_charge():
    """
    Cria uma cobrança PIX imediata (sem txid).
    """
    try:
        token_data = get_access_token()
        access_token = token_data['access_token']

        # Endpoint para criar a cobrança
        url = f"{PIX_API_BASE}/v2/cob"
        
        data = request.json
        payload = {
            "calendario": {"expiracao": 3600},  # Validade de 1 hora
            "devedor": {
                "cpf": data.get("cpf"),
                "nome": data.get("nome")
            },
            "valor": {"original": f"{data['value']:.2f}"},
            "chave": "chave-exemplo",  # Substitua pela sua chave PIX
            "solicitacaoPagador": data.get("description", "Cobrança PIX")
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers, cert=certificado)
        response.raise_for_status()

        return jsonify(response.json()), 201

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro na comunicação com a API PIX: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pix/charge/<txid>', methods=['GET'])
def get_pix_charge_status(txid):
    """
    Consulta o status de uma cobrança PIX.
    """
    try:
        token_data = get_access_token()
        access_token = token_data['access_token']

        url = f"{PIX_API_BASE}/v2/cob/{txid}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers, cert=certificado)
        response.raise_for_status()
        
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400

# ---------------------------------------------- ENDPOINTS DE PIX COM VENCIMENTO ----------------------------------------------

@app.route('/pix/charge/due', methods=['POST'])
def create_pix_due_charge():
    """
    Cria uma cobrança PIX com vencimento.
    """
    try:
        token_data = get_access_token()
        access_token = token_data['access_token']

        url = f"{PIX_API_BASE}/v2/cobv"
        
        data = request.json
        payload = {
            "calendario": {
                "dataDeVencimento": data.get("dataDeVencimento"),
                "validadeAposVencimento": data.get("validadeAposVencimento", 30)
            },
            "devedor": {
                "logradouro": data.get("logradouro"),
                "cidade": data.get("cidade"),
                "uf": data.get("uf"),
                "cep": data.get("cep"),
                "cpf": data.get("cpf"),
                "nome": data.get("nome")
            },
            "valor": {
                "original": f"{data['valor']:.2f}",
                "multa": {
                    "modalidade": 2,
                    "valorPerc": str(data.get("multa", {}).get("valorPerc", "0.00"))
                },
                "juros": {
                    "modalidade": 2,
                    "valorPerc": str(data.get("juros", {}).get("valorPerc", "0.00"))
                },
                "desconto": {
                    "modalidade": 1,
                    "descontoDataFixa": [
                        {
                            "data": data.get("desconto", {}).get("data"),
                            "valorPerc": str(data.get("desconto", {}).get("valorPerc", "0.00"))
                        }
                    ]
                }
            },
            "chave": "chave-exemplo",  # Substitua pela sua chave PIX
            "solicitacaoPagador": data.get("solicitacaoPagador", "Cobrança PIX")
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers, cert=certificado)
        response.raise_for_status()

        return jsonify(response.json()), 201

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro na comunicação com a API PIX: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pix/charge/update/<txid>', methods=['PATCH'])
def update_pix_due_charge(txid):
    """
    Atualiza uma cobrança PIX com vencimento existente.
    """
    try:
        token_data = get_access_token()
        access_token = token_data['access_token']

        url = f"{PIX_API_BASE}/v2/cobv/{txid}"

        data = request.json
        payload = {
            "loc": {
                "id": data.get("loc_id")
            },
            "devedor": {
                "logradouro": data.get("logradouro"),
                "cidade": data.get("cidade"),
                "uf": data.get("uf"),
                "cep": data.get("cep"),
                "cpf": data.get("cpf"),
                "nome": data.get("nome")
            },
            "valor": {
                "original": f"{data['valor']:.2f}"
            },
            "solicitacaoPagador": data.get("solicitacaoPagador", "Cobrança revisada")
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.patch(url, json=payload, headers=headers, cert=certificado)
        response.raise_for_status()

        return jsonify(response.json()), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro na comunicação com a API PIX: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pix/charge/status/<txid>', methods=['GET'])
def get_pix_due_charge_status(txid):
    """
    Consulta o status de uma cobrança PIX com vencimento.
    """
    try:
        token_data = get_access_token()
        access_token = token_data['access_token']

        url = f"{PIX_API_BASE}/v2/cobv/{txid}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers, cert=certificado)
        response.raise_for_status()

        return jsonify(response.json()), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro na comunicação com a API PIX: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------- ENDPOINTS DE GESTÃO DE PIX ----------------------------------------------

@app.route('/pix/<e2e_id>', methods=['GET'])
def get_pix(e2e_id):
    """
    Endpoint para consultar um Pix através do e2eId.
    """
    try:
        token_data = get_access_token()
        access_token = token_data['access_token']

        url = f"{PIX_API_BASE}/v2/pix/{e2e_id}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers, cert=certificado)
        response.raise_for_status()

        return jsonify(response.json()), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400

@app.route('/pix', methods=['GET'])
def get_pix_list():
    """
    Endpoint para consultar vários Pix recebidos.
    """
    try:
        token_data = get_access_token()
        access_token = token_data['access_token']

        inicio = request.args.get('inicio')
        fim = request.args.get('fim')

        if not inicio or not fim:
            return jsonify({"error": "Os parâmetros 'inicio' e 'fim' são obrigatórios."}), 400

        # URL para consultar os Pix
        url = f"{PIX_API_BASE}/v2/pix?inicio={inicio}&fim={fim}"

        # Cabeçalhos da requisição
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers, cert=certificado)
        response.raise_for_status()

        return jsonify(response.json()), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400

@app.route('/pix/<e2e_id>/devolucao/<refund_id>', methods=['PUT'])
def request_pix_refund(e2e_id, refund_id):
    """
    Endpoint para solicitar uma devolução de Pix.
    """
    try:
        token_data = get_access_token()
        access_token = token_data['access_token']

        url = f"{PIX_API_BASE}/v2/pix/{e2e_id}/devolucao/{refund_id}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.put(url, headers=headers, cert=certificado)
        response.raise_for_status()

        return jsonify(response.json()), 201

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400

@app.route('/pix/<e2e_id>/devolucao/<refund_id>', methods=['GET'])
def get_refund_status(e2e_id, refund_id):
    """
    Endpoint para consultar o status de uma devolução de Pix.
    """
    try:
        token_data = get_access_token()
        access_token = token_data['access_token']

        url = f"{PIX_API_BASE}/v2/pix/{e2e_id}/devolucao/{refund_id}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers, cert=certificado)
        response.raise_for_status()

        return jsonify(response.json()), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400

# ---------------------------------------------- Webhook para notificação do envio de Pix ----------------------------------------------

def process_pix_notification(notification_data):
    """
    Processa a notificação de pagamento PIX.
    """
    try:
        status = notification_data.get("status")
        txid = notification_data.get("txid")
        valor_pago = notification_data.get("valor", {}).get("original")
        devedor_nome = notification_data.get("devedor", {}).get("nome")

        # Aqui você pode fazer a lógica necessária com os dados recebidos
        # Exemplo: atualizar o status da cobrança no banco de dados
        if status == "PAID":
            # Marcar como pago, por exemplo, em uma tabela de cobranças
            print(f"A cobrança {txid} foi paga no valor de R${valor_pago} por {devedor_nome}.")
            # Aqui seria o local para atualizar seu banco de dados ou sistema
        elif status == "CANCELLED":
            print(f"A cobrança {txid} foi cancelada.")
        else:
            print(f"A cobrança {txid} tem status: {status}")

    except Exception as e:
        print(f"Erro ao processar a notificação: {e}")

@app.route('/pix/webhook', methods=['POST'])
def pix_webhook():
    """
    Webhook para receber notificações de pagamento PIX.
    """
    try:
        if request.is_json:
            notification_data = request.get_json()
            
            process_pix_notification(notification_data)
            
            return jsonify({"status": "sucesso", "message": "Notificação processada com sucesso!"}), 200
        else:
            return jsonify({"status": "erro", "message": "Formato inválido, esperado JSON."}), 400

    except Exception as e:
        return jsonify({"status": "erro", "message": f"Erro ao processar a notificação: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
