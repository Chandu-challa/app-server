import psycopg2

conn = psycopg2.connect(
    dbname="customer_db",
    user="postgres",
    password="12345678",
    host="127.0.0.1",
    port="5433"
)

print("Connected successfully!")