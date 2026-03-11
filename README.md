# API de Controle de Estoque (Flask + MySQL)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey?style=for-the-badge&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql)

## Sobre o Projeto
Este projeto é uma **API RESTful** desenvolvida para simular o backend de um sistema de gerenciamento de estoque real. 

O objetivo principal foi unir a lógica de programação (Python) com a persistência de dados (MySQL), criando um sistema capaz de realizar todas as operações **CRUD** (Create, Read, Update, Delete) de forma eficiente e segura.

Diferente de projetos básicos que usam listas em memória, este sistema **persiste os dados**, garantindo que as informações de produtos, preços e quantidades não se percam ao reiniciar o servidor.

---

## Arquitetura e Fluxo

O sistema segue a arquitetura cliente-servidor, onde o Flask atua como o intermediário que recebe as requisições HTTP, processa as regras de negócio e conversa com o banco de dados.

```mermaid
graph TD;
    A[Cliente (Insomnia/Curl)] -->|Requisição HTTP| B(Flask API);
    B -->|SQL Query| C[(MySQL Database)];
    C -->|Dados| B;
    B -->|JSON Response| A;
```

---

## Como Rodar o Projeto

### Pré-requisitos
- Python 3.8+
- MySQL rodando localmente (ou em servidor)

### 1. Clone o repositório e instale as dependências

```bash
git clone https://github.com/Matheusfelislino/sistema_estoque_flask.git
cd sistema_estoque_flask
pip install -r requirements.txt
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Abra o arquivo `.env` e preencha com suas credenciais:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=estoque_db
FLASK_DEBUG=false
```

### 3. Crie o banco de dados

Execute o script SQL no seu MySQL:

```bash
mysql -u root -p < schema.sql
```

### 4. Inicie a API

```bash
python run.py
```

A API estará disponível em `http://localhost:5001`.

---

## Rodando os Testes

Os testes utilizam **pytest** e não exigem conexão real com o banco de dados (a camada de model é mockada).

```bash
pytest
```

Para rodar com saída detalhada:

```bash
pytest -v
```

---

## Estrutura do Projeto

```
sistema_estoque_flask/
├── api/
│   ├── database/
│   │   └── connection.py       # Conexão com o banco de dados
│   ├── models/
│   │   └── produto.py          # Funções de acesso ao banco (CRUD)
│   ├── routes/
│   │   └── produtos.py         # Endpoints da API
│   └── validators/
│       └── produto_validator.py # Validações de entrada
├── tests/
│   ├── conftest.py             # Fixtures compartilhadas do pytest
│   └── test_produtos.py        # Testes automatizados dos endpoints
├── run.py                      # Ponto de entrada da aplicação
├── schema.sql                  # Script de criação do banco de dados
├── .env.example                # Modelo de variáveis de ambiente
├── pytest.ini                  # Configuração do pytest
└── requirements.txt            # Dependências do projeto
```

---

## Endpoints da API

| Método | Rota | Descrição | Exemplo de Body (JSON) |
| :--- | :--- | :--- | :--- |
| **GET** | `/produtos` | Lista todos os produtos (aceita filtros) | *Nenhum* |
| **GET** | `/produtos/<id>` | Busca um produto pelo ID | *Nenhum* |
| **POST** | `/produtos` | Cadastra um novo produto | `{"nome": "Mouse", "preco": 50.00}` |
| **PUT** | `/produtos/<id>` | Substituição completa (quantidade + preço) | `{"quantidade": 20, "preco": 45.00}` |
| **PATCH** | `/produtos/<id>` | Atualização parcial de qualquer campo | `{"preco": 45.00}` |
| **DELETE**| `/produtos/<id>` | Remove um produto | *Nenhum* |

### Filtros disponíveis em GET /produtos

| Query param | Exemplo | Descrição |
| :--- | :--- | :--- |
| `nome` | `/produtos?nome=Mouse` | Busca parcial pelo nome |
| `marca` | `/produtos?marca=Logitech` | Busca parcial pela marca |
| `estoque_baixo` | `/produtos?estoque_baixo=true` | Retorna apenas produtos com quantidade = 0 |

### Formato de Resposta

Todas as respostas seguem o padrão:

**Sucesso:**
```json
{
  "success": true,
  "message": "Descrição da operação",
  "data": { ... }
}
```

**Erro:**
```json
{
  "success": false,
  "message": "Descrição do erro",
  "data": null,
  "errors": ["Detalhe do erro 1", "Detalhe do erro 2"]
}
```

---

## Melhorias Futuras

- [ ] Autenticação via JWT
- [ ] Paginação na listagem de produtos
- [ ] Documentação interativa via Swagger/Flasgger
- [ ] Deploy em Render ou Railway

---
Desenvolvido por **Matheus**
