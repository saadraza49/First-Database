from fastapi import FastAPI , Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User

