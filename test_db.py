import mysql.connector
from config import DB_CONFIG

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    if conn.is_connected():
        print("Sucesso! Conetado ao banco estoque_db no MYSQL.")

        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print(f"Você está conectado ao banco: {record[0]}")

        cursor.close()
        conn.close()
except Exception as e:
    print(f"Erro ao conectar; {e}")
