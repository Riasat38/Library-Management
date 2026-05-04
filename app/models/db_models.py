from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Enum
from app.database import Base
from sqlalchemy.orm import relationship
import datetime 
import enum

class BookDB(Base):
    __tablename__ = "books"

    # Primary Key (auto-incrementing ID)
    id = Column(Integer, primary_key=True, index=True)
    
    # Book Details
    title = Column(String)
    author = Column(String)
    pages = Column(Integer)
    
    # ISBN is unique and indexed for fast searching
    isbn = Column(String, unique=True, index=True, nullable=False)
    publish_year = Column(Integer)
    genre = Column(String)
    
    # Status
    available = Column(Boolean, default=True)

    borrows = relationship("BorrowDB", back_populates="book")

class BorrowStatus(str, enum.Enum):
    active = "active"
    returned = "returned"

class MemberDB(Base):
    __tablename__ = "members"

    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String, nullable=False)
    email           = Column(String, unique=True, index=True, nullable=False)
    phone           = Column(String, nullable=True)
    membership_date = Column(Date, default=datetime.date.today)
    is_active       = Column(Boolean, default=True)

    # one member → many borrow records
    borrows         = relationship("BorrowDB", back_populates="member")


class BorrowDB(Base):
    __tablename__ = "borrows"

    id          = Column(Integer, primary_key=True, index=True)
    book_id     = Column(Integer, ForeignKey("books.id"), nullable=False)
    member_id   = Column(Integer, ForeignKey("members.id"), nullable=False)
    borrow_date = Column(Date, default=datetime.date.today)
    due_date    = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)   # null until the book is returned
    status      = Column(Enum(BorrowStatus), default=BorrowStatus.active)

    # navigate from a borrow record directly to the full book or member object
    book        = relationship("BookDB", back_populates="borrows")
    member      = relationship("MemberDB", back_populates="borrows")