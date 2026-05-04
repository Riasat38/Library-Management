from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    title: str
    author: str
    pages: int 
    isbn: str
    publish_year: Optional[int] = None
    genre: Optional[str] = None
    available: bool = True

# Schema for updates — all fields optional so you can partially update
class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    pages: int | None = None
    available: bool | None = None
    publish_year: Optional[int] = None

class BookResponse(BaseModel):
    id        : int
    isbn      : str
    title     : str
    author    : str
    publish_year: Optional[int]
    genre: Optional[str]
    available : bool

    class Config:
        from_attributes = True