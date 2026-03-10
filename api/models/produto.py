from api.database.connection import get_db_connection


def get_all_produtos():
    """Retorna todos os produtos do banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    return produtos


def get_produto_by_id(produto_id: int):
    """Busca um produto pelo ID no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos WHERE id = %s", (produto_id,))
    produto = cursor.fetchone()
    cursor.close()
    conn.close()
    return produto


def create_produto(nome: str, marca: str, preco: float, quantidade: int):
    """Cria um novo produto no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = (
        "INSERT INTO produtos (nome, marca, preco, quantidade) "
        "VALUES (%s, %s, %s, %s)"
    )
    cursor.execute(query, (nome, marca, preco, quantidade))
    conn.commit()
    novo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return novo_id


def update_produto(produto_id: int, quantidade: int, preco: float):
    """Atualiza quantidade e preço de um produto no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE produtos SET quantidade = %s, preco = %s WHERE id = %s"
    cursor.execute(query, (quantidade, preco, produto_id))
    conn.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    conn.close()
    return rows_affected


def delete_produto(produto_id: int):
    """Remove um produto do banco de dados pelo ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = %s", (produto_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    conn.close()
    return rows_affected
