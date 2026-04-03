# First Database

I created this project to practice database management using SQLAlchemy and FastAPI. I will portray everything I did step by step.

## Step 1: Setting up the environment

I created a virtual environment to manage dependencies.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Setting up the database

I created a database using PostgreSQL.

```bash
CREATE DATABASE postgres;
```

## Step 3: Setting up the database connection

I created a database connection using SQLAlchemy.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:postgres@IP_ADDRESS/postgres")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

## Step 4: Creating the User model

I created a User model using SQLAlchemy.

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
```

## Step 5: Alembic

I used alembic to manage the database migrations.
First I initialized alembic.
```bash
alembic init alembic
```
Then I created a migration file.
```bash
alembic revision --autogenerate -m "create user table"
```
Then I applied the migration.
```bash
alembic upgrade head
```

## Step 6: Creating the FastAPI app

I created a FastAPI app to serve the data.
```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Product

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/products")
def read_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
```

## Step 7: Running the app

I ran the app using uvicorn.
```bash
uvicorn main:app --reload
```

