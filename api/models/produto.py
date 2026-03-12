from api.database.connection import get_db_connection


def get_all_produtos():
    """Retorna todos os produtos do banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM produtos")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_produto_by_id(produto_id: int):
    """Busca um produto pelo ID no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM produtos WHERE id = %s", (produto_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def create_produto(nome: str, marca: str, preco: float, quantidade: int):
    """Cria um novo produto no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            INSERT INTO produtos (nome, marca, preco, quantidade)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (nome, marca, preco, quantidade))
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()


def update_produto(produto_id: int, quantidade: int, preco: float):
    """Atualiza quantidade e preço de um produto no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            UPDATE produtos
            SET quantidade = %s, preco = %s
            WHERE id = %s
        """
        cursor.execute(query, (quantidade, preco, produto_id))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()


def delete_produto(produto_id: int):
    """Remove um produto do banco de dados pelo ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM produtos WHERE id = %s", (produto_id,))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()