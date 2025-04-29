from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

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

class BookRequest(BaseModel):
    id: Optional[int] = Field(default=None, title="Book ID", description="The ID is not need on create")
    title: str = Field(min_length=3, title="Book Title", description="The title of the book", example="Book Title")
    author: str = Field(min_length=3, title="Book Author", description="The author of the book", example="Author Name")
    description: str = Field(min_length=1, max_length=100, title="Book Description", description="A brief description of the book", example="This is a great book.")
    rating: int = Field(gt=0, lt=6, title="Book Rating", description="The rating of the book", example=5)

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


@app.post("/create-book")
async def create_book(book_request : BookRequest):
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))
    return book_request


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book