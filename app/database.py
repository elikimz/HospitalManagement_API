from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure asyncpg is used for async operations
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Fix: Add `connect_args={"ssl": True}`
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True, connect_args={"ssl": True})

# Create session factory
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# Base class for models
Base = declarative_base()

# Fix: Async function for getting session
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
        await db.close()  # Proper async closing
