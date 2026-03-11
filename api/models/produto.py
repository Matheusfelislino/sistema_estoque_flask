import logging

import mysql.connector

from api.database.connection import get_db_connection

logger = logging.getLogger(__name__)


def get_all_produtos(nome: str = None, marca: str = None, estoque_baixo: bool = False):
    """Retorna todos os produtos do banco de dados, com filtros opcionais.

    Args:
        nome: Filtro parcial pelo nome do produto (LIKE %nome%).
        marca: Filtro parcial pela marca do produto (LIKE %marca%).
        estoque_baixo: Se True, retorna apenas produtos com quantidade == 0.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            conditions = []
            params = []

            if nome:
                conditions.append("nome LIKE %s")
                params.append(f"%{nome}%")
            if marca:
                conditions.append("marca LIKE %s")
                params.append(f"%{marca}%")
            if estoque_baixo:
                conditions.append("quantidade = 0")

            query = "SELECT * FROM produtos"
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()
    except mysql.connector.Error as exc:
        logger.error("Erro ao listar produtos: %s", exc)
        raise
    finally:
        conn.close()


def get_produto_by_id(produto_id: int):
    """Busca um produto pelo ID no banco de dados."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM produtos WHERE id = %s", (produto_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
    except mysql.connector.Error as exc:
        logger.error("Erro ao buscar produto %s: %s", produto_id, exc)
        raise
    finally:
        conn.close()


def create_produto(nome: str, marca: str, preco: float, quantidade: int):
    """Cria um novo produto no banco de dados."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        try:
            query = (
                "INSERT INTO produtos (nome, marca, preco, quantidade) "
                "VALUES (%s, %s, %s, %s)"
            )
            cursor.execute(query, (nome, marca, preco, quantidade))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
    except mysql.connector.Error as exc:
        logger.error("Erro ao criar produto: %s", exc)
        raise
    finally:
        conn.close()


def update_produto(produto_id: int, quantidade: int, preco: float):
    """Atualiza quantidade e preço de um produto no banco de dados (substituição completa)."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        try:
            query = "UPDATE produtos SET quantidade = %s, preco = %s WHERE id = %s"
            cursor.execute(query, (quantidade, preco, produto_id))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
    except mysql.connector.Error as exc:
        logger.error("Erro ao atualizar produto %s: %s", produto_id, exc)
        raise
    finally:
        conn.close()


def patch_produto(produto_id: int, fields: dict):
    """Atualiza parcialmente um produto no banco de dados.

    Args:
        produto_id: ID do produto a ser atualizado.
        fields: Dicionário com os campos e novos valores a serem atualizados.
    """
    allowed = {"nome", "marca", "preco", "quantidade"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return 0

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        try:
            set_clause = ", ".join(f"{col} = %s" for col in updates)
            params = list(updates.values()) + [produto_id]
            query = f"UPDATE produtos SET {set_clause} WHERE id = %s"
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
    except mysql.connector.Error as exc:
        logger.error("Erro ao fazer patch no produto %s: %s", produto_id, exc)
        raise
    finally:
        conn.close()


def delete_produto(produto_id: int):
    """Remove um produto do banco de dados pelo ID."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM produtos WHERE id = %s", (produto_id,))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
    except mysql.connector.Error as exc:
        logger.error("Erro ao deletar produto %s: %s", produto_id, exc)
        raise
    finally:
        conn.close()
