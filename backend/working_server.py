#!/usr/bin/env python3
"""
Working registration server without database
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

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

# In-memory storage for testing
users_db = []
next_id = 1

@app.post("/api/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """Register a new user"""
    global next_id

    # Check if user already exists
    for user in users_db:
        if user["username"] == user_data.username or user["email"] == user_data.email:
            raise HTTPException(
                status_code=400,
                detail="Username or email already registered"
            )

    # Create new user
    new_user = {
        "id": next_id,
        "username": user_data.username,
        "email": user_data.email,
        "password": "hashed_password_here",  # In real app, hash this
        "full_name": user_data.full_name,
        "role": user_data.role,
        "is_active": True,
        "created_at": "2024-01-01T00:00:00Z"
    }

    users_db.append(new_user)
    next_id += 1

    return UserResponse(**new_user)

@app.get("/")
async def root():
    return {"message": "Working Registration Server"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/auth/register")
async def get_register_info():
    return {"message": "POST to this endpoint to register a new user"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
