from fastapi import FastAPI, Query
import requests
import os
from dotenv import load_dotenv
from database import get_connection
import time

# Load environment variables
load_dotenv()

app = FastAPI()

# 🔗 Flask API URL (from .env)
FLASK_API = os.getenv("FLASK_API_URL")


# 🏠 Home API
@app.get("/")
def home():
    return {"message": "FastAPI is working 🚀"}


# 📄 Get customers from Flask (Dynamic Pagination)


@app.get("/customers")
def get_customers(page: int = Query(1), limit: int = Query(10)):
    """
    Fetch customers from Flask API with retries.
    """
    max_retries = 3
    backoff = 2  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.get(f"{FLASK_API}?page={page}&limit={limit}", timeout=20)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(backoff)  # wait before retrying
                backoff *= 2  # exponential backoff
            else:
                return {
                    "error": f"Failed to fetch from Flask API after {max_retries} attempts.",
                    "details": str(e)
                }


# 🔥 Ingest data from Flask → PostgreSQL
@app.api_route("/ingest", methods=["GET", "POST"])
def ingest_data():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        response = requests.get(
            f"{FLASK_API}?page=1&limit=20",
            timeout=20
        )

        response.raise_for_status()

        data = response.json().get("data", [])

        for c in data:
            cursor.execute("""
                INSERT INTO customers (
                    customer_id, first_name, last_name, email,
                    phone, address, date_of_birth,
                    account_balance, created_at
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (customer_id) DO NOTHING
            """, (
                c.get("customer_id"),
                c.get("first_name"),
                c.get("last_name"),
                c.get("email"),
                c.get("phone"),
                c.get("address"),
                c.get("date_of_birth"),
                c.get("account_balance"),
                c.get("created_at")
            ))

        conn.commit()

        cursor.close()
        conn.close()

        return {"message": "Data inserted successfully"}

    except Exception as e:
        return {"error": f"Ingestion failed: {str(e)}"}


# 📊 Fetch data from Database
@app.get("/db/customers")
def get_db_customers():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()

        result = [
            {
                "customer_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "phone": row[4],
                "address": row[5],
                "date_of_birth": str(row[6]),
                "account_balance": float(row[7]),
                "created_at": str(row[8])
            }
            for row in rows
        ]

        cursor.close()
        conn.close()

        return {"data": result}

    except Exception as e:
        return {"error": f"Database fetch failed: {str(e)}"}
