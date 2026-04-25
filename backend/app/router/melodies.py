from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app import crud, schemas
from app.db import get_db

from app.router.auth import get_current_active_admin

router = APIRouter(prefix="/melodies", tags=["melodies"])

@router.post("", response_model=schemas.Melody)
def create_melody(
    melody: schemas.MelodyCreate, 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    return crud.create_melody(db=db, melody=melody)

@router.put("/{melody_id}", response_model=schemas.Melody)
def update_melody(
    melody_id: int, 
    melody_update: Dict[str, Any] = Body(...), 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    db_melody = crud.update_melody(db, melody_id=melody_id, melody_update=melody_update)
    if not db_melody:
        raise HTTPException(status_code=404, detail="Melody not found")
    return db_melody

@router.get("", response_model=List[schemas.Melody])
def read_melodies(
    skip: int = 0, 
    limit: int = 100, 
    village: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    melodies = crud.get_melodies(db, skip=skip, limit=limit, village=village, category=category, search=search)
    return melodies

@router.get("/count")
def get_melodies_count(
    village: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return {"total": crud.count_melodies(db, village=village, category=category, search=search)}

@router.get("/search")
def search_melodies(search: str, db: Session = Depends(get_db)):
    return crud.get_melodies_by_search(db, search)

@router.get("/{melody_id}", response_model=schemas.Melody)
def read_melody(melody_id: int, db: Session = Depends(get_db)):
    db_melody = crud.get_melody(db, melody_id=melody_id)
    if db_melody is None:
        raise HTTPException(status_code=404, detail="Melody not found")
    return db_melody

@router.delete("/{melody_id}")
def delete_melody(
    melody_id: int, 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    success = crud.delete_melody(db, melody_id=melody_id)
    if not success:
        raise HTTPException(status_code=404, detail="Melody not found")
    return {"message": "Melody deleted successfully"}
