from fastapi import FastAPI
from .database import  Base
from .routes import auth  # Import your routes
from app.database import sync_engine as engine, Base


# Create database tables (if not using Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Management System API")

# Include routers

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hospital Management API is running 🚀"}
