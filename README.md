# Flask PIX API
<div style="text-align: center;">
  <img src="https://yt3.googleusercontent.com/4aXZ2E2tM-iXAOfCyQ6Av_zbfvETsScxRhTm68YaFrfl05jG3cS0KHRu2rX-UsYHH1iR8SPg=s900-c-k-c0x00ffffff-no-rj" width="300" />
</div>

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
- Arquivo requirements.txt com as dependências necessárias.

## Instalação e Configuração do Ambiente

Siga os passos abaixo para configurar o ambiente e instalar as dependências necessárias para rodar a aplicação:

1. **Crie um ambiente virtual (venv):**

   Em um terminal, navegue até o diretório do projeto e execute o seguinte comando para criar o ambiente virtual:

   ```bash
   python3 -m venv venv

## Obtendo suas credenciais
Um integrador pode criar quantas aplicações desejar. Para cada aplicação são gerados 2 pares de chaves ```Client_Id``` e ```Client_Secret```, sendo um par para utilização em ambiente de Produção e outro para Homologação.

### Para isso basta criar uma aplicação ou configurar uma já existente
Veja como criar uma aplicação ou aproveitar uma aplicação já existente para integrar com a API Pix Efí.

### Criando uma aplicação:
Para criar uma aplicação para utilização da API Pix siga os passos abaixo:

1. Acesse sua conta e clique no item "API" na parte inferior do menu à esquerda da conta Efí;
2. Clique em "Criar aplicação"
3. Habilite a API Pix e escolha os escopos que deseja liberar em ambiente de Produção e Homologação (você pode editá-los no futuro);
4. Com os escopos selecionados, clique em "Continuar".
![Imagem 1](https://dev.efipay.com.br/img/criacao_aplicacao_pix.png)

### Aproveitando uma aplicação já existente:
Para aproveitar uma aplicação já cadastrada em sua conta e usá-la para a integração com Pix, siga os passos abaixo:

1. Acesse sua conta e clique no item "API" na parte inferior do menu à esquerda da conta Efí;
2. Clique em "Aplicações". Em seguida, escolha a aplicação que será editada, clique nos três pontinhos e depois em configurações;
3. Habilite a API Pix e escolha os escopos que deseja liberar em ambiente de Produção e Homologação (você pode editá-los sempre que quiser);
4. Com os escopos selecionados, clique em "Continuar".
![Imagem 1](https://dev.efipay.com.br/img/edicao_aplicacao_pix.png)
![Imagem 2](https://dev.efipay.com.br/img/criacao_aplicacao_pix.png)

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
   git clone https://github.com/AlvaroSalvino/api-efi-pay.git
   cd api-efi-pay
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
    Caso o certificado.pem esteja na raiz do projeto seria:

    ```python
    certificado = './certificado.pem'
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
python app.py
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
