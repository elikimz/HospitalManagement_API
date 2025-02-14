from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure DATABASE_URL is in the correct format for asyncpg
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create Base
Base = declarative_base()

# Create async engine
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create session factory
async_session_factory = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with async_session_factory() as session:
        yield session
