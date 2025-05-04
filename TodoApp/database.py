from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy database URL
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos-app.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  

# PostgreSQL database URL
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5433/TodoApplicationDatabase'  # Replace with your PostgreSQL credentials
# engine = create_engine(SQLALCHEMY_DATABASE_URL)  

# MySQL database URL
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:root@localhost:3306/todoapplicationdatabase'  # Replace with your MySQL credentials
engine = create_engine(SQLALCHEMY_DATABASE_URL)  

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()