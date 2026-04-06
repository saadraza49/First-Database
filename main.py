from fastapi import FastAPI , Depends , HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class UserBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str

class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.post("/create_users")
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

@app.get("/users/{user_id}")
def read_user(id: int , db: Session = Depends(get_db)):
    student = db.query(User).filter(User.id == id).first()
    if not student:
        raise HTTPException(status_code=404 , detail="User not found")
    return student

@app.delete("/delete_user/{user_id}")
def delete_user(id: int , db: Session = Depends(get_db)):
    student = db.query(User).filter(User.id == id).first()
    if not student:
        raise HTTPException(status_code=404 , detail="User not found")
    db.delete(student)
    db.commit()
    return {"message":"User deleted successfully"}

@app.put("/update_user/{user_id}")
def update_user(id:int , user:UpdateUser , db:Session = Depends(get_db)):
    student = db.query(User).filter(User.id == id).first()
    if not student:
        raise HTTPException(status_code=404 , detail="User not found")
    student.first_name = user.first_name
    student.last_name = user.last_name
    student.age = user.age
    student.email = user.email
    db.commit()
    db.refresh(student)
    return {"message":"User updated successfully"}