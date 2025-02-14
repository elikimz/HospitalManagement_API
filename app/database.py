from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import ssl
from.config import settings  # adjust the import as needed

# Convert to asyncpg URL if needed
raw_url = settings.database_url
if raw_url.startswith("postgresql://"):
    raw_url = raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Parse the URL and remove the 'sslmode' parameter if necessary
from sqlalchemy.engine.url import make_url
url_obj = make_url(raw_url)
query_params = dict(url_obj.query)
if "sslmode" in query_params:
    query_params.pop("sslmode")
    url_obj = url_obj._replace(query=query_params)

modified_url = str(url_obj)
print("Modified URL:", modified_url)

# Create an SSL context for secure connection
ssl_context = ssl.create_default_context()

# Create the async engine with the SSL context
async_engine = create_async_engine(
    modified_url,
    echo=True,
    connect_args={"ssl": ssl_context}
)

# Create the async session factory
async_session_factory = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with async_session_factory() as session:
        yield session
