from flask import Flask, jsonify, request
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def home():
    return "<h1>API de Estoque Rodando! </h1><p>Acesse <a href='/produtos'>/produtos</a> para ver a lista.</p>"

@app.route("/produtos", methods=["GET"])
def listar_produtos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(produtos)

@app.route("/produtos", methods=["POST"])
def criar_produto():
    novo_produto = request.get_json()

    if not novo_produto or "nome" not in novo_produto or "preco" not in novo_produto:
        return jsonify({"erro": "Dados inválidos. Precisa de 'nome' e 'preco'"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "INSERT INTO produtos (nome, marca, preco, quantidade) VALUES (%s, %s, %s, %s)"
    valores = (
        novo_produto["nome"],
        novo_produto.get("marca",""),
        novo_produto["preco"],
        novo_produto.get("quantidade", 0)
    )
    cursor.execute(query, valores)
    conn.commit()

    id_novo = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({"mensagem": "Produto criado com sucesso!", "id": id_novo }),201

@app.route("/produto/<int:id_produto>", methods=["PUT"])
def atualizar_produto(id_produto):
    dados = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "UPDATE produtos SET quantidade = %s, preco = %s WHERE id = %s"
    valores = (dados["quantidade"], dados["preco"], id_produto)

    cursor.execute(query, valores)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensagem": "Estoque atualizado com sucesso!"})

@app.route("/produto/<int:id_produto>", methods=["DELETE"])
def deletar_produto(id_produto):
    conn = get_db_connection
    cursor = conn.cursor()

    query = "DELETE FROM produtos WHERE id = %s"
    cursor.execute(query, (id_produto,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensagem": "Produto deletado com sucesso!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
