from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db_models import BookDB
from app.models.book import Book, BookUpdate

# In-memory database (temporary)
books_db = {}

# Initialize the router
router = APIRouter()

# Routes

@router.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: Book, db: Session = Depends(get_db)):

    db_book = db.query(BookDB).filter(BookDB.isbn == book.isbn).first()
    if db_book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Book with ISBN '{book.isbn}' already exists"
        )
    new_book = BookDB(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {'msg': f"Book '{book.title}' created successfully", "data": book}

#get all books
@router.get("/books")
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(BookDB).all()
    return {"data": books}

#get a book
@router.get("/books/{isbn}")
def get_book(isbn: str, db:Session = Depends(get_db)):
    db_book = db.query(BookDB).filter(BookDB.isbn == isbn).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ISBN '{isbn}' not found"
        )
    return {"data": db_book}


@router.put("/books/{isbn}")
def update_book(isbn: str, book_update: BookUpdate, db: Session = Depends(get_db)):

    db_book = db.query(BookDB).filter(BookDB.isbn == isbn).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ISBN '{isbn}' not found"
        )
    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    #existing_book = books_db[isbn]
    #update_data = book_update.model_dump(exclude_unset=True)
    #updated_book = existing_book.model_copy(update=update_data)
    #books_db[isbn] = updated_book
    return {"msg": f"Book '{db_book.title}' updated successfully", "data": db_book}


@router.delete("/books/{isbn}", status_code=status.HTTP_200_OK)
def delete_book(isbn: str, db:Session = Depends(get_db)):
    db_book = db.query(BookDB).filter(BookDB.isbn == isbn).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ISBN '{isbn}' not found"
        )
    db.delete(db_book)
    db.commit()
    #deleted_book = books_db.pop(isbn)
    return {"msg": f"Book deleted successfully"}