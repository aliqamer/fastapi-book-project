from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer, default=1)  # Default priority is set to 1
    completed = Column(Boolean, default=False)

    # def __repr__(self):
    #     return f"<Todo(id={self.id}, title={self.title}, description={self.description}, completed={self.completed})>"  
    
