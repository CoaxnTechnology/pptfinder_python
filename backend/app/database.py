from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from fastapi import HTTPException


# ============================
# Validate DATABASE_URL
# ============================
if not settings.DATABASE_URL:
    raise Exception(
        "❌ ERROR: DATABASE_URL is missing.\n"
        "Make sure your .env file contains:\n"
        "DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DBNAME"
    )


# ============================
# Create PostgreSQL Engine
# ============================
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,            # Check stale DB connections
        pool_size=10,                  # Optional performance tuning
        max_overflow=20,               # Handles heavy traffic spikes
        echo=False                     # Set True for SQL logs
    )
except Exception as e:
    raise Exception(f"❌ Failed to create engine: {e}")


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
