from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app import crud, schemas
from app.db import get_db

from app.router.auth import get_current_active_admin

router = APIRouter(prefix="/artists", tags=["artists"])

@router.post("", response_model=schemas.Artist)
def create_artist(
    artist: schemas.ArtistCreate, 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    return crud.create_artist(db=db, artist=artist)

@router.put("/{artist_id}", response_model=schemas.Artist)
def update_artist(
    artist_id: int, 
    artist_update: Dict[str, Any] = Body(...), 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    db_artist = crud.update_artist(db, artist_id=artist_id, artist_update=artist_update)
    if not db_artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return db_artist

@router.get("", response_model=List[schemas.Artist])
def read_artists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_artists(db, skip=skip, limit=limit)

@router.get("/count")
def get_artists_count(db: Session = Depends(get_db)):
    return {"total": crud.count_artists(db)}

@router.get("/{artist_id}", response_model=schemas.Artist)
def read_artist(artist_id: int, db: Session = Depends(get_db)):
    db_artist = crud.get_artist(db, artist_id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return db_artist

@router.delete("/{artist_id}")
def delete_artist(
    artist_id: int, 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    success = crud.delete_artist(db, artist_id=artist_id)
    if not success:
        raise HTTPException(status_code=404, detail="Artist not found")
    return {"message": "Artist deleted successfully"}
