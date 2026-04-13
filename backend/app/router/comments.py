from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas, security
from app.db import get_db
from app.router.auth import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/", response_model=List[schemas.Comment])
def read_comments(
    melody_id: Optional[int] = None,
    article_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    return crud.get_comments(db, melody_id=melody_id, article_id=article_id, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Comment)
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_comment(db=db, comment=comment, user_id=current_user.id)
