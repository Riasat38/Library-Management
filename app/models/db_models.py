from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class BookDB(Base):
    __tablename__ = "books"

    # Primary Key (auto-incrementing ID)
    id = Column(Integer, primary_key=True, index=True)
    
    # Book Details
    title = Column(String)
    author = Column(String)
    pages = Column(Integer)
    
    # ISBN is unique and indexed for fast searching
    isbn = Column(String, unique=True, index=True)
    
    # Status
    available = Column(Boolean, default=True)
