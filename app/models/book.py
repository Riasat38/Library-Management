from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    pages: int 
    isbn: str
    available: bool = True

# Schema for updates — all fields optional so you can partially update
class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    pages: int | None = None
    available: bool | None = None