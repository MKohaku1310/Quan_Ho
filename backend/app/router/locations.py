from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app import crud, schemas, models
from app.db import get_db

from app.router.auth import get_current_active_admin

router = APIRouter(prefix="/locations", tags=["locations"])

@router.post("", response_model=schemas.Location)
def create_location(
    location: schemas.LocationCreate, 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    return crud.create_location(db=db, location=location)

@router.put("/{location_id}", response_model=schemas.Location)
def update_location(
    location_id: int, 
    location_update: Dict[str, Any] = Body(...), 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    db_loc = crud.update_location(db, location_id=location_id, location_update=location_update)
    if not db_loc:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_loc

@router.delete("/{location_id}")
def delete_location(
    location_id: int, 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    success = crud.delete_location(db, location_id=location_id)
    if not success:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"message": "Location deleted successfully"}

@router.get("", response_model=List[schemas.Location])
def read_locations(
    skip: int = 0, 
    limit: int = 100, 
    type: Optional[str] = None,
    district: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    locations = crud.get_locations(db, skip=skip, limit=limit, type=type, district=district, search=search)
    for loc in locations:
        if not loc.featured_songs:
            melodies = db.query(models.Melody).filter(models.Melody.village == loc.name).limit(3).all()
            if melodies:
                loc.featured_songs = ", ".join([m.name for m in melodies if m.name])
    return locations

@router.get("/count")
def get_locations_count(
    type: Optional[str] = None,
    district: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return {"total": crud.count_locations(db, type=type, district=district, search=search)}

@router.get("/{location_id}", response_model=schemas.Location)
def read_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    if not db_location.featured_songs:
        melodies = db.query(models.Melody).filter(models.Melody.village == db_location.name).limit(5).all()
        if melodies:
            db_location.featured_songs = ", ".join([m.name for m in melodies if m.name])
    return db_location
