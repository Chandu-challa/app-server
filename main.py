from fastapi import FastAPI, Query
import requests
from database import get_connection

app = FastAPI()

# 🔗 Flask API URL
FLASK_API = "https://mock-server-x04f.onrender.com/api/customers"


# 🏠 Home API
@app.get("/")
def home():
    return {"message": "FastAPI is working 🚀"}


# 📄 Get customers from Flask (Dynamic Pagination)
@app.get("/customers")
def get_customers(page: int = Query(1), limit: int = Query(10)):
    try:
        response = requests.get(f"{FLASK_API}?page={page}&limit={limit}")
        
        if response.status_code != 200:
            return {"error": "Failed to fetch data from Flask"}

        return response.json()

    except Exception as e:
        return {"error": str(e)}


# 🔥 Ingest data from Flask → PostgreSQL
@app.post("/ingest")
def ingest_data():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        response = requests.get(f"{FLASK_API}?page=1&limit=20")

        if response.status_code != 200:
            return {"error": "Failed to fetch data from Flask"}

        data = response.json()["data"]

        for c in data:
            cursor.execute("""
                INSERT INTO customers (
                    customer_id, first_name, last_name, email,
                    phone, address, date_of_birth,
                    account_balance, created_at
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (customer_id) DO NOTHING
            """, (
                c["customer_id"],
                c["first_name"],
                c["last_name"],
                c["email"],
                c["phone"],
                c["address"],
                c["date_of_birth"],
                c["account_balance"],
                c["created_at"]
            ))

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Data inserted successfully"}

    except Exception as e:
        return {"error": str(e)}


# 📊 Fetch data from Database
@app.get("/db/customers")
def get_db_customers():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                "customer_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "phone": row[4],
                "address": row[5],
                "date_of_birth": str(row[6]),
                "account_balance": float(row[7]),
                "created_at": str(row[8])
            })

        cursor.close()
        conn.close()

        return {"data": result}

    except Exception as e:
        return {"error": str(e)}