import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="customer_db",
        user="postgres",
        password="12345678",
        host="127.0.0.1",
        port="5433"
    )