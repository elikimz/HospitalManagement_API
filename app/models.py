from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

# User roles
class UserRole(enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    RECEPTIONIST = "receptionist"
    PHARMACIST = "pharmacist"
    PATIENT = "patient"

# User Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False) 
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient_profile = relationship("Patient", back_populates="user", uselist=False)
    staff_profile = relationship("Staff", back_populates="user", uselist=False)

# Patient Model
class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String, nullable=False)
    dob = Column(DateTime, nullable=False)
    contact = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="patient_profile")
    appointments = relationship("Appointment", back_populates="patient")
    billing = relationship("Billing", back_populates="patient")

# Staff Model
class Staff(Base):
    __tablename__ = "staff"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="staff_profile")
    appointments = relationship("Appointment", back_populates="doctor")

# Appointment Model
class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(String, default="scheduled")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Staff", back_populates="appointments")

# Billing Model
class Billing(Base):
    __tablename__ = "billing"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="Unpaid")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="billing")
    payments = relationship("Payment", back_populates="billing")

# Payment Model
class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    billing_id = Column(Integer, ForeignKey("billing.id"), nullable=False)
    amount_paid = Column(Float, nullable=False)
    method = Column(String, default="M-Pesa")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    billing = relationship("Billing", back_populates="payments")

# Medicine Model
class Medicine(Base):
    __tablename__ = "medicines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Prescription Model
class Prescription(Base):
    __tablename__ = "prescriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    dosage = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    doctor = relationship("Staff")
    patient = relationship("Patient")
    medicine = relationship("Medicine")

# Reports Model
class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String, nullable=False)
    details = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
