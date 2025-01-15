# Flask PIX API

## Descrição

Este projeto é uma aplicação Flask que fornece endpoints para interagir com a API PIX da Gerencianet. Ele permite:

- Autenticação e obtenção de token de acesso;
- Criação e consulta de cobranças PIX imediatas e com vencimento;
- Consulta e gestão de transações PIX;
- Solicitação de devoluções de pagamentos via PIX.

## Pré-requisitos

- Python 3.8 ou superior;
- Flask;
- Requests;
- Um certificado no formato PEM para autenticação com a API PIX;
- Arquivo `requirements.txt` com as dependências necessárias.

## Gerando um certificado P12
Para gerar o seu certificado, basta seguir os passos abaixo:

1. Acesse o item "API" no menu inferior à esquerda da conta Efí;
2. No menu à esquerda, clique em "Meus Certificados";
3. Na nova janela, selecione o ambiente ao qual pertencerá o certificado (Produção ou Homologação);
4. Clique em "Novo Certificado" (botão azul);
5. Atribua uma descrição ao certificado para identificá-lo no futuro;
6. Confirme a criação do certificado;
7. Por fim, baixe o certificado e clique em prosseguir.

Os passos para a criação de um certificado estão ilustrados nas imagens a seguir.

![Imagem 1](https://dev.efipay.com.br/img/passos_para_criar_certificado.png)
![Imagem 2](https://dev.efipay.com.br/img/janela_criacao_certificado.png)
![Imagem 3](https://dev.efipay.com.br/img/download_certificado.png)

Vale ressaltar que um mesmo certificado pode ser usado por diversas aplicações da sua conta digital. Ainda assim, você pode gerar até cinco certificados para cada ambiente (Produção ou Homologação).

## Configuração do Certificado

Ao baixar um certificado, ele geralmente vem no formato P12. Para utilizá-lo em formato PEM, siga os passos abaixo:

1. No projeto, há um arquivo compactado com o nome **'conversor-p12-efi-main.zip'**. Descompacte este arquivo.
2. Coloque o arquivo de certificado **.P12** na mesma pasta que o arquivo **'conversor-p12-efi-main.bat'**.
3. Execute o arquivo **'conversor-p12-efi-main.bat'**.
4. Insira o nome do seu certificado (sem a extensão **.P12**).
5. O processo irá gerar um novo arquivo de certificado no formato **.PEM**, que é o arquivo a ser utilizado.

Este será o certificado adequado para sua configuração.

## Configuração Inicial

1. Clone este repositório:

   ```bash
   git clone <url-do-repositorio>
   cd flask-pix-api
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure suas credenciais no dicionário `credentials` no arquivo principal do projeto:

   ```python
   credentials = {
       "client_id": "seu_client_id",
       "client_secret": "seu_client_secret",
   }
   ```

4. Adicione o caminho para o seu certificado no formato PEM:

   ```python
   certificado = './caminho/para/seu/certificado.pem'
   ```

5. Escolha entre usar a URL de homologação ou produção:

   - Para homologação (testes):

     ```python
     PIX_API_BASE = "https://pix-h.api.efipay.com.br"
     ```

   - Para produção:

     ```python
     PIX_API_BASE = "https://pix.api.efipay.com.br"
     ```

## Executando a Aplicação

Inicie a aplicação Flask:

```bash
python <nome_do_arquivo>.py
```

A API estará disponível em `http://localhost:5000` por padrão.

## Endpoints

### Autenticação

#### `GET /auth`

Obtém o token de acesso para interagir com a API PIX.

**Resposta:**

```json
{
  "access_token": "seu_token"
}
```

### Cobranças PIX Imediatas

#### `POST /pix/charge`

Cria uma cobrança PIX imediata.

**Parâmetros do corpo (JSON):**

```json
{
  "cpf": "12345678901",
  "nome": "Nome do Cliente",
  "value": 100.50,
  "description": "Descrição opcional da cobrança"
}
```

**Resposta:**

Detalhes da cobrança criada.

### Cobranças PIX com Vencimento

#### `POST /pix/charge/due`

Cria uma cobrança PIX com vencimento.

**Parâmetros do corpo (JSON):**

```json
{
  "dataDeVencimento": "2024-12-31",
  "validadeAposVencimento": 30,
  "logradouro": "Rua Exemplo",
  "cidade": "Exemplo",
  "uf": "EX",
  "cep": "12345000",
  "cpf": "12345678901",
  "nome": "Nome do Cliente",
  "valor": 150.75,
  "multa": {"valorPerc": 2},
  "juros": {"valorPerc": 1},
  "desconto": {"data": "2024-12-25", "valorPerc": 5},
  "solicitacaoPagador": "Pagamento do serviço X"
}
```

**Resposta:**

Detalhes da cobrança criada.

### Consulta de Transações PIX

#### `GET /pix/<e2e_id>`

Consulta detalhes de um PIX específico através do e2eId.

**Resposta:**

Detalhes da transação PIX.

#### `GET /pix`

Consulta múltiplos PIX recebidos.

**Parâmetros de URL:**

- `inicio`: Data de início (formato ISO8601);
- `fim`: Data de fim (formato ISO8601).

**Resposta:**

Lista de transações PIX.

### Devoluções de PIX

#### `PUT /pix/<e2e_id>/devolucao/<refund_id>`

Solicita a devolução de um PIX.

**Parâmetros do corpo (JSON):**

```json
{
  "valor": 50.00
}
```

**Resposta:**

Detalhes da devolução.

## Observações

- Certifique-se de proteger suas credenciais e certificado.
- Use os endpoints de homologação para testes antes de mudar para produção.

## Licença

Este projeto está licenciado sob a licença MIT.
