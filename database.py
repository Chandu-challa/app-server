import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="customer_db",
        user="postgres",
        password="12345678",
        host=" https://app-server-aigs.onrender.com/db/customers",
        port="5433"
    )