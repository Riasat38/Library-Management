from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.db_models import MemberDB
from app.models.member import MemberCreate, MemberUpdate, MemberResponse

router = APIRouter(prefix="/members", tags=["Members"])


# ── POST /members ──────────────────────────────────────────────────────────────

@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def register_member(member: MemberCreate, db: Session = Depends(get_db)):
    # check if email already exists
    existing = db.query(MemberDB).filter(MemberDB.email == member.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A member with email '{member.email}' already exists."
        )

    new_member = MemberDB(
        name  = member.name,
        email = member.email,
        phone = member.phone,
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


# ── GET /members ───────────────────────────────────────────────────────────────

@router.get("/", response_model=list[MemberResponse])
def get_all_members(db: Session = Depends(get_db)):
    return db.query(MemberDB).all()

#get all active
@router.get("/active", response_model=list[MemberResponse])
def get_active_members(db: Session = Depends(get_db)):
    return db.query(MemberDB).filter(MemberDB.is_active == True).all()

#get all inactive
@router.get("/inactive", response_model=list[MemberResponse])
def get_inactive_members(db: Session = Depends(get_db)):
    return db.query(MemberDB).filter(MemberDB.is_active == False).all()

# ── GET /members/{id} ──────────────────────────────────────────────────────────

@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(MemberDB).filter(MemberDB.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found."
        )
    return member


# ── PUT /members/{id} ──────────────────────────────────────────────────────────

@router.put("/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, updates: MemberUpdate, db: Session = Depends(get_db)):
    member = db.query(MemberDB).filter(MemberDB.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found."
        )

    # only update fields that were actually sent
    if updates.name is not None:
        member.name = updates.name
    if updates.phone is not None:
        member.phone = updates.phone

    db.commit()
    db.refresh(member)
    return member


# ── DELETE /members/{id} — soft delete only ────────────────────────────────────

@router.delete("/{member_id}", status_code=status.HTTP_200_OK)
def deactivate_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(MemberDB).filter(MemberDB.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found."
        )
    if not member.is_active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Member with id {member_id} is already deactivated."
        )

    member.is_active = False
    db.commit()
    return {"message": f"Member '{member.name}' has been deactivated."}


##need permanent delete feature