from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # Default role is set to "user"

    # def __repr__(self):
    #     return f"<User(id={self.id}, username={self.username}, email={self.email})>"

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer, default=1)  # Default priority is set to 1
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to Users table

    # def __repr__(self):
    #     return f"<Todo(id={self.id}, title={self.title}, description={self.description}, completed={self.completed})>"  
    
