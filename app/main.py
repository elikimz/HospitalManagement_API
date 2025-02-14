from fastapi import FastAPI
from .database import async_engine, Base
from .routes import auth  # Import your routes

# Create database tables (if not using Alembic)
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(title="Hospital Management System API")

# Include routers
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hospital Management API is running 🚀"}

# Run table creation at startup
import asyncio
@app.on_event("startup")
async def startup():
    await create_tables()
