# Running the Project (Backend + Mobile App)

This guide provides instructions to set up and run the entire project, including the **FastAPI backend**, **PostgreSQL database**, **Docker containers**, and the **mobile application**.

---

## 🛠 Prerequisites

- **Docker & Docker Compose** installed
- **Python & Uvicorn** installed
- **pgAdmin** (optional, for database management)

---

## 🚀 Running the Project

### 1️⃣ Start the FastAPI Backend

from project root:

```bash
uvicorn api.main:app --reload
```

### 2️⃣ Build and Start Docker Containers

```bash
docker-compose up --build
```

or, separately:

```bash
docker-compose build
docker-compose up
```

### 3️⃣ Verify Running Containers

```bash
docker-compose ps
```

### 4️⃣ Stopping the Project

In case you want to stop the project

```bash
docker-compose down
```

---

## 🔹 Interacting with the FastAPI Container

To enter the FastAPI container and run commands:

```bash
docker exec -it fastapi_app bash
```

---

## 🧪 Running Tests

Inside the FastAPI container, run:

- **Single test file:**
  ```bash
  pytest tests/test_data_loader.py
  pytest tests/test_data_processor.py
  pytest tests/test_feature_extractor.py
  pytest tests/test_step_prediction_pipeline.py
  pytest tests/test_steps_predictor.py
  ```
- **All tests in the `tests` directory:**
  ```bash
  pytest tests
  ```
- **Ignore warnings while testing:**
  ```bash
  pytest -W ignore::FutureWarning tests/test_data_loader.py
  ```

---

## 🗃️ Database Management

### Access PostgreSQL via Terminal

```bash
docker exec -it postgres_db psql -U db_temp_user -d step_detection_db
```

To view table contents:

```sql
SELECT * FROM predictions;
```

### Create `predictions` Table

usually it creates automatically (so no need to run the following)

```sql
CREATE TABLE predictions (
    id VARCHAR PRIMARY KEY,
    start_time VARCHAR,
    end_time VARCHAR,
    left_steps INTEGER,
    right_steps INTEGER,
    timestamp TIMESTAMP
);
```

---

## 🌍 Accessing the Database via pgAdmin

1. Open **pgAdmin** at [http://localhost:5050](http://localhost:5050)
2. Login:
   - **Email:** `admin@admin.com`
   - **Password:** `admin`
3. Connect to PostgreSQL:
   - Click **"Add New Server"**
   - **General Tab:** Name: `PostgresDB`
   - **Connection Tab:**
     - **Hostname:** `db` (Docker) or `localhost` (local PostgreSQL)
     - **Port:** `5432`
     - **Username:** `db_temp_user`
     - **Password:** `db_temp_pass`
     - Click **Save**
4. Navigate to **Databases → step_detection_db → Schemas → public → Tables → predictions**
5. Right-click `predictions` → **View Data → All Rows**

---

## 🌐 Accessing the Application

### FastAPI Backend

- Open [http://localhost:8000](http://localhost:8000)

### API Documentation (Swagger UI)

- Open [http://localhost:8000/docs](http://localhost:8000/docs)

### PostgreSQL Connection

- Connect to **localhost:5432** using a PostgreSQL client

---

## 📱 Mobile Application (Android)

- If the container is **running**, the app has full functionality.
- If the container is **not running**, only the JSON file-based features will work (prediction & API calls won’t function).

---

Let's go -> 🚀
