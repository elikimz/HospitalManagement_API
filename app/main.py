from fastapi import FastAPI
from app.database import engine, Base
from app.routes import users, patients, appointments  # Import your routes

# Create database tables (if not using Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Management System API")

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])

@app.get("/")
def root():
    return {"message": "Hospital Management API is running 🚀"}
