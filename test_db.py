from api.database.connection import get_db_connection

try:
    conn = get_db_connection()
    if conn.is_connected():
        print("Sucesso! Conectado ao banco estoque_db no MYSQL.")

        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print(f"Você está conectado ao banco: {record[0]}")

        cursor.close()
        conn.close()
except Exception as e:
    print(f"Erro ao conectar: {e}")
