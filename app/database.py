from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure asyncpg is used for FastAPI
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine for FastAPI
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

# Create sync engine for Alembic migrations
sync_engine = create_engine(DATABASE_URL, echo=True)

# Create async session for FastAPI
SessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# Base class for models
Base = declarative_base()

# Dependency to get DB session (for FastAPI)
async def get_db():
    async with SessionLocal() as db:
        yield db
