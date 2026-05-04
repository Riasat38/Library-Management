from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from app.models.db_models import BorrowStatus


# ── Member Schemas ─────────────────────────────────────────────────────────────

class MemberCreate(BaseModel):
    """What the client sends when registering a new member."""
    name  : str
    email : EmailStr
    phone : Optional[str] = None


class MemberUpdate(BaseModel):
    """All fields optional — client only sends what they want to change."""
    name  : Optional[str] = None
    phone : Optional[str] = None


class MemberResponse(BaseModel):
    """What the API sends back."""
    id              : int
    name            : str
    email           : str
    phone           : Optional[str]
    membership_date : date
    is_active       : bool

    class Config:
        from_attributes = True  # allows building from SQLAlchemy ORM objects


# ── Nested schemas (used inside BorrowResponse) ────────────────────────────────

class BookSummary(BaseModel):
    """Minimal book info embedded inside a borrow record response."""
    id     : int
    title  : str
    author : str
    isbn   : str

    class Config:
        from_attributes = True


class MemberSummary(BaseModel):
    """Minimal member info embedded inside a borrow record response."""
    id    : int
    name  : str
    email : str

    class Config:
        from_attributes = True


# ── Borrow Schemas ─────────────────────────────────────────────────────────────

class BorrowCreate(BaseModel):
    """What the client sends when borrowing a book."""
    book_id   : int
    member_id : int


class BorrowResponse(BaseModel):
    """What the API sends back for a borrow record."""
    id          : int
    borrow_date : date
    due_date    : date
    return_date : Optional[date]
    status      : BorrowStatus
    book        : BookSummary    # nested — full book info inside the response
    member      : MemberSummary  # nested — full member info inside the response

    class Config:
        from_attributes = True