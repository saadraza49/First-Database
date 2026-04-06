from fastapi import FastAPI , Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users")
def create_user(user: UserBase , db: Session = Depends(get_db)):
    db_user = User(
        first_name=user.first_name, 
        last_name=user.last_name,
        age=user.age,
        email=user.email
    ) 
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
