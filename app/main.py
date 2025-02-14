from fastapi import FastAPI
from .database import  Base
from .routes import users, patients, appointments,auth  # Import your routes
from app.database import sync_engine as engine, Base


# Create database tables (if not using Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Management System API")

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hospital Management API is running 🚀"}
