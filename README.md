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

## Por dentro do Código (Explicação Técnica)

Aqui destaco as partes mais importantes da lógica desenvolvida:

### 1. Conexão Modularizada (`config.py`)
Para evitar hardcode de senhas no arquivo principal e facilitar a manutenção, separei as credenciais do banco.
> **Por que isso é importante?** Em um ambiente real, isso permite que mudemos o banco de desenvolvimento para o de produção sem tocar no código da aplicação.

### 2. Tratamento de Dados no Cadastro (POST)
No endpoint de criação de produtos, utilizei o método `.get()` do Python para evitar erros caso o cliente esqueça de enviar campos opcionais.
```python
# Exemplo do código:
valores = (
    novo_produto['nome'],          # Obrigatório
    novo_produto.get('marca', ''), # Opcional (se não vier, fica vazio)
    novo_produto['preco'],         # Obrigatório
    novo_produto.get('quantidade', 0) # Opcional (padrão é 0)
```

## Endpoints da API

Aqui estão as rotas disponíveis para teste (via Postman, Insomnia ou Curl).

| Método | Rota | Descrição | Exemplo de Body (JSON) |
| :--- | :--- | :--- | :--- |
| **GET** | `/produtos` | Lista todos os produtos | *Nenhum* |
| **POST** | `/produtos` | Cadastra um novo produto | `{"nome": "Mouse", "preco": 50.00}` |
| **PUT** | `/produtos/<id>` | Atualiza estoque e preço | `{"quantidade": 20, "preco": 45.00}` |
| **DELETE**| `/produtos/<id>` | Remove um produto | *Nenhum* |

---
Desenvolvido por **Matheus** 
