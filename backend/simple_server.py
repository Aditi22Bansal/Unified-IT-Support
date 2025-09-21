#!/usr/bin/env python3
"""
Simple test server for registration endpoint
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from passlib.context import CryptContext
import enum
import uvicorn

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Enums
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    SUPPORT_AGENT = "support_agent"
    CUSTOMER = "customer"

# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    role: str = "customer"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: str

    class Config:
        from_attributes = True

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """Register a new user"""
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.username == user_data.username) | (User.email == user_data.email)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Username or email already registered"
            )

        # Create new user
        hashed_password = pwd_context.hash(user_data.password)

        # Map role string to UserRole enum
        role_mapping = {
            "customer": UserRole.CUSTOMER,
            "support_agent": UserRole.SUPPORT_AGENT,
            "admin": UserRole.ADMIN
        }
        user_role = role_mapping.get(user_data.role.lower(), UserRole.CUSTOMER)

        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=user_role
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Simple Registration Test Server"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
