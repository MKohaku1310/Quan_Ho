from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas, security, models
from app.db import get_db
from app.router.auth import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("", response_model=List[schemas.Comment])
def read_comments(
    melody_id: Optional[int] = None,
    article_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    return crud.get_comments(db, melody_id=melody_id, article_id=article_id, skip=skip, limit=limit)

@router.get("/count")
def get_comments_count(
    melody_id: Optional[int] = None,
    article_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return {"total": crud.count_comments(db, melody_id=melody_id, article_id=article_id)}

@router.post("", response_model=schemas.Comment)
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    if (comment.melody_id is None) == (comment.article_id is None):
        raise HTTPException(status_code=422, detail="Exactly one of melody_id or article_id is required")
    return crud.create_comment(db=db, comment=comment, user_id=current_user.id)
@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Check permissions: Admin or Owner
    role_value = getattr(current_user.role, "value", current_user.role)
    if role_value != "admin" and db_comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    
    success = crud.delete_comment(db, comment_id=comment_id)
    return {"message": "Comment deleted successfully"}
