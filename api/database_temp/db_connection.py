from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.prediction_model import Base

# Database URL (replace with your PostgreSQL credentials)
DATABASE_URL = "postgresql+asyncpg://db_user:db_password@localhost/step_detection_db"

# This creates a synchronous database engine using SQLAlchemy's create_engine function.
# sync_engine = create_engine("postgresql://user:password@localhost/dbname")

# Create an async engine and session
async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
