import os
import ssl
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine.url import make_url
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Convert to asyncpg URL if needed
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Parse the URL to remove the unsupported 'sslmode' parameter
url = make_url(DATABASE_URL)
query = dict(url.query)
if "sslmode" in query:
    query.pop("sslmode")
    url = url._replace(query=query)

# Create an SSL context for secure connection
ssl_context = ssl.create_default_context()
# You can customize the SSL context if needed:
# ssl_context.check_hostname = False
# ssl_context.verify_mode = ssl.CERT_NONE

# Create the async engine with the SSL context provided via connect_args
async_engine = create_async_engine(
    str(url),
    echo=True,
    future=True,
    connect_args={"ssl": ssl_context}
)

# Create session factory for async sessions
async_session_factory = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency to get DB session (for FastAPI)
async def get_db():
    async with async_session_factory() as session:
        yield session
