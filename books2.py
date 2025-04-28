from fastapi import Body, FastAPI, HTTPException
#from pydantic import BaseModel, Field

app = FastAPI()

class Book():
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

BOOKS = [
    Book(id=1, title="Book One", author="Author A", description="Description of Book One", rating=4),
    Book(id=2, title="Book Two", author="Author B", description="Description of Book Two", rating=5),
    Book(id=3, title="Book Three", author="Author C", description="Description of Book Three", rating=3),
    Book(id=4, title="Book Four", author="Author D", description="Description of Book Four", rating=2),
    Book(id=5, title="Book Five", author="Author E", description="Description of Book Five", rating=1),
    Book(id=6, title="Book Six", author="Author F", description="Description of Book Six", rating=5),
    Book(id=7, title="Book Seven", author="Author G", description="Description of Book Seven", rating=4),
]

@app.get("/books")
async def get_all_books():
    return BOOKS