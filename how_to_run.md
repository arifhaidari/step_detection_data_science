# How to run the whole project (Backend + Mobile App)

use a bash script in order to run everything smooth including:
fastapi, database, run container and connect everything

run the fastapi app:
uvicorn api.main:app --reload

build and start docker container:
docker-compose up --build
or:
docker-compose build
docker-compose up

check if the both containers running:
docker-compose ps

seeing the tables in terminal:
docker exec -it postgres_db psql -U db_temp_user -d step_detection_db
SELECT \* FROM predictions;
create table using terminal:
CREATE TABLE predictions (
id VARCHAR PRIMARY KEY,
start_time VARCHAR,
end_time VARCHAR,
left_steps INTEGER,
right_steps INTEGER,
timestamp TIMESTAMP
);

to see the table using browser:
use pgadmin
http://localhost:5050
username: admin@admin.com
password: admin

Login with:

Email: admin@admin.com
Password: admin
Connect to Your PostgreSQL Database:

Click "Add New Server"
General Tab → Enter Server Name: PostgresDB
Connection Tab →
Hostname: db (if using Docker) or localhost (if PostgreSQL is installed locally)
Port: 5432
Username: db_temp_user
Password: db_temp_pass
Click Save
Now, navigate to Databases → step_detection_db → Schemas → public → Tables → predictions
Right-click predictions → View Data → All Rows to see all saved records.

access the app:
FastAPI: Open http://localhost:8000 in your browser.
PostgreSQL: Connect to localhost:5432 using a PostgreSQL client.
to access the swagger ui:
http://localhost:8000/docs
