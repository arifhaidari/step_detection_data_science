# AWS Deployment

Link to services deployed on AWS cloud service:

- **FastAPI:**  
  [http://54.164.146.71:8000/docs](http://54.164.146.71:8000/docs)  
  _Note: It might ask you to continue even though it is not secure (HTTP)._

---

## 🌍 Accessing the Database via pgAdmin

1. Open **pgAdmin** at [http://54.164.146.71:5050](http://54.164.146.71:5050).
2. **Login Credentials:**
   - **Email:** `admin@admin.com`
   - **Password:** `admin`
3. **Connect to PostgreSQL:**
   - Click **"Add New Server"**.
   - **General Tab:**
     - **Name:** `PostgresDB`
   - **Connection Tab:**
     - **Hostname:** `db` (Docker) or `localhost` (local PostgreSQL)
     - **Port:** `5432`
     - **Username:** `db_temp_user`
     - **Password:** `db_temp_pass`
     - Click **Save**.
4. Navigate to **Databases → step_detection_db → Schemas → public → Tables → predictions**.
5. Right-click on `predictions` and select **View Data → All Rows**.
