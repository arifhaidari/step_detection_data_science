import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import MetaData, Table, Column, String, Integer, DateTime, Float
from databases import Database

# Load environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://db_temp_user:db_temp_pass@db:5432/step_detection_db")

# Create an asynchronous SQLAlchemy engine
async_engine = create_async_engine(DATABASE_URL, echo=True)
metadata = MetaData()

# Define the predictions table
predictions_table = Table(
    "predictions",
    metadata,
    Column("id", String, primary_key=True),
    Column("start_time", String),
    Column("end_time", String),
    Column("left_steps", Integer),
    Column("right_steps", Integer),
    Column("num_measurements", Integer),
    Column("session_duration", Float),
    Column("timestamp", DateTime),
)

# Create a database instance for async queries
database = Database(DATABASE_URL)

# Create the table (run this once to create the table in the database)
async def create_tables():
     async with async_engine.begin() as conn:
          await conn.run_sync(metadata.create_all)

# Dependency to get the database connection
async def get_db():
     await database.connect()
     try:
          yield database
     finally:
          await database.disconnect()