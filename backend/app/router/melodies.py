from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas
from app.db import get_db

router = APIRouter(prefix="/melodies", tags=["melodies"])

@router.post("/", response_model=schemas.Melody)
def create_melody(melody: schemas.MelodyCreate, db: Session = Depends(get_db)):
    return crud.create_melody(db=db, melody=melody)

@router.get("/", response_model=List[schemas.Melody])
def read_melodies(
    skip: int = 0, 
    limit: int = 100, 
    village: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    melodies = crud.get_melodies(db, skip=skip, limit=limit, village=village, category=category)
    return melodies

@router.get("/{melody_id}", response_model=schemas.Melody)
def read_melody(melody_id: int, db: Session = Depends(get_db)):
    db_melody = crud.get_melody(db, melody_id=melody_id)
    if db_melody is None:
        raise HTTPException(status_code=404, detail="Melody not found")
    return db_melody

@router.get("/search/")
def search_melodies(search: str, db: Session = Depends(get_db)):
    return crud.get_melodies_by_search(db, search)
