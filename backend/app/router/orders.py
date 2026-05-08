from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app import crud, schemas, models
from app.db import get_db
from app.router import auth
from app.router.auth import get_current_active_admin

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=schemas.Order)
def create_order(
    order: schemas.OrderCreate, 
    db: Session = Depends(get_db),
    current_user: Optional[schemas.User] = Depends(auth.get_current_user_optional)
):
    try:
        user_id = current_user.id if current_user else None
        return crud.create_order(db=db, order=order, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[schemas.Order])
def read_orders(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    # Members see their own orders, Admin sees all
    if current_user.role == models.UserRole.admin:
        return crud.get_orders(db, skip=skip, limit=limit)
    return crud.get_orders(db, skip=skip, limit=limit, user_id=current_user.id)

@router.get("/all", response_model=List[schemas.Order])
def read_all_orders(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    return crud.get_orders(db, skip=skip, limit=limit)

@router.get("/count")
def get_orders_count(db: Session = Depends(get_db), admin: schemas.User = Depends(get_current_active_admin)):
    return {"total": crud.count_orders(db)}

@router.get("/{order_id}", response_model=schemas.Order)
def read_order(
    order_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    db_order = crud.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check permission
    if current_user.role != models.UserRole.admin and db_order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    return db_order

@router.patch("/{order_id}/status", response_model=schemas.Order)
def update_order_status(
    order_id: int, 
    status: models.OrderStatus = Body(..., embed=True), 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    db_order = crud.update_order_status(db, order_id, status)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
