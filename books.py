from fastapi import Body, FastAPI, HTTPException

app = FastAPI()

BOOKS = [
        {"id": 1, "title": "1984", "author": "George Orwell", "category": "Dystopian"},
        {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Fiction"},
        {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Classic"},
        {"id": 4, "title": "Brave New World", "author": "Aldous Huxley", "category": "Dystopian"}
    ]

@app.get("/books")
async def get_books_from_db():
    # Simulate a database call
    return BOOKS

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int):
    # Simulate a database call
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/{book_title}/title")
async def get_book_by_title(book_title: str):
    # Simulate a database call
    for book in BOOKS:
        if book["title"].lower() == book_title.lower():
            return book
    raise HTTPException(status_code=404, detail="Book not found")   

@app.get("/books/{book_author}/author")
async def get_book_by_author(book_author: str, category: str = None):
    books_to_return = []
    # Simulate a database call
    for book in BOOKS:
        if book["author"].lower() == book_author.lower():
            if category and book["category"].lower() == category.lower():
                books_to_return.append(book)
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books")
async def add_book(book: dict):
    # Simulate a database call
    new_book = book.copy()
    new_book["id"] = len(BOOKS) + 1
    BOOKS.append(new_book)
    return new_book

@app.put("/books/{book_id}")
async def update_book(book_id: int, book: dict):
    # Simulate a database call
    for index, existing_book in enumerate(BOOKS):
        if existing_book["id"] == book_id:
            BOOKS[index].update(book)
            return BOOKS[index]
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/update_book")
async def update_book_by_title(updated_book: Body()):
    # Simulate a database call
    for index, book in enumerate(BOOKS):
        if book["title"].lower() == updated_book["title"].lower():
            BOOKS[index].update(updated_book)
            return BOOKS[index]
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    # Simulate a database call
    for index, book in enumerate(BOOKS):
        if book["id"] == book_id:
            del BOOKS[index]
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")