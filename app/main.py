from fastapi import FastAPI
from app.routes import auth  # Import your routes
# from app.database import sync_engine as engine  # Ensure you're using the correct engine
# from app.database import Base  # Import Base once

app = FastAPI(title="Hospital Management System API")

# Include routers
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hospital Management API is running 🚀"}
