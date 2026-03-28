# 🚀 Backend Developer Technical Assessment

This project implements a **data pipeline system** using **Flask**, **FastAPI**, and **PostgreSQL**, with full Docker support and live deployment.

---

## 🌐 Live Application Links

### 🔹 FastAPI Pipeline Service

👉 https://app-server-aigs.onrender.com

### 🔹 Flask Mock Server

👉 https://mock-server-x04f.onrender.com/

---

## 🧩 Architecture Overview

```id="arch1"
Flask Mock Server → FastAPI Pipeline → PostgreSQL Database → API Response
```

---

## ⚙️ Tech Stack

* Python 3.10+
* Flask
* FastAPI
* PostgreSQL
* SQLAlchemy
* Docker & Docker Compose

---

## 📁 Project Structure

```id="arch2"
project-root/
│
├── docker-compose.yml
├── README.md
│
├── mock-server/
│
└── pipeline-service/
```

---

## 🚀 How It Works

1. Flask API serves customer data from JSON
2. FastAPI fetches data from Flask (handles pagination)
3. Data is processed and stored in PostgreSQL
4. FastAPI exposes APIs to access stored data

---

## 🔗 API Endpoints

### ✅ Mock Server (Flask)

* GET `/api/customers?page=1&limit=10`
* GET `/api/customers/{id}`
* GET `/api/health`

📌 Example:

```id="ex1"
curl https://mock-server-x04f.onrender.com/api/customers?page=1&limit=5
```

---

### ✅ Pipeline Service (FastAPI)

* POST `/api/ingest`
* GET `/api/customers?page=1&limit=10`
* GET `/api/customers/{id}`

📌 Examples:

**Ingest Data**

```id="ex2"
curl -X POST https://app-server-aigs.onrender.com/api/ingest
```

**Fetch Customers**

```id="ex3"
curl https://app-server-aigs.onrender.com/api/customers?page=1&limit=5
```

---

## ✅ Features Implemented

* ✔ Flask mock API with JSON data
* ✔ Pagination support
* ✔ FastAPI ingestion pipeline
* ✔ PostgreSQL integration
* ✔ Upsert logic (update if exists)
* ✔ Dockerized architecture
* ✔ Live deployment of both services

---

## 🧪 Testing Flow

1. Call ingestion API
2. Data is fetched from Flask API
3. Stored in PostgreSQL
4. Retrieve using FastAPI endpoints

---

## ⚠️ Notes

* FastAPI automatically handles pagination while ingesting data
* Duplicate records are avoided using upsert logic

---

## 📌 Author

**Chandu Challa**

---

## 🎯 Summary

This project demonstrates:

* Microservices architecture
* API development using Flask & FastAPI
* Data ingestion pipeline
* Database handling with PostgreSQL
* Docker-based deployment
* Live production deployment

---
