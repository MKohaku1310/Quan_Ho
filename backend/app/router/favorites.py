from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.db import get_db
from app.router.auth import get_current_user

router = APIRouter(prefix="/favorites", tags=["favorites"])

@router.get("", response_model=List[schemas.FavoriteItem])
def read_favorites(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.get_favorites(db, current_user.id)

@router.post("", response_model=schemas.FavoriteItem)
def add_favorite(
    payload: schemas.FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    favorite = crud.create_favorite(db, current_user.id, payload.melody_id)
    if not favorite:
        raise HTTPException(status_code=404, detail="Melody not found")
    return favorite

@router.delete("/{melody_id}")
def remove_favorite(
    melody_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    ok = crud.delete_favorite(db, current_user.id, melody_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return {"message": "Favorite removed"}
