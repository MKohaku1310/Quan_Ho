from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app import crud, schemas, models
from app.db import get_db

from app.router.auth import get_current_active_admin

router = APIRouter(prefix="/articles", tags=["articles"])

@router.post("", response_model=schemas.Article)
def create_article(
    article: schemas.ArticleCreate, 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    return crud.create_article(db=db, article=article, author_id=admin.id)

@router.put("/{article_id}", response_model=schemas.Article)
def update_article(
    article_id: int, 
    article_update: Dict[str, Any] = Body(...), 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    db_art = crud.update_article(db, article_id=article_id, article_update=article_update)
    if not db_art:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_art

@router.delete("/{article_id}")
def delete_article(
    article_id: int, 
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_current_active_admin)
):
    success = crud.delete_article(db, article_id=article_id)
    if not success:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "Article deleted successfully"}

@router.get("", response_model=List[schemas.Article])
def read_articles(
    skip: int = 0, 
    limit: int = 100, 
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_articles(db, skip=skip, limit=limit, category=category, search=search)

@router.get("/count")
def get_articles_count(category: Optional[str] = None, search: Optional[str] = None, db: Session = Depends(get_db)):
    return {"total": crud.count_articles(db, category=category, search=search)}

@router.get("/{article_id}", response_model=schemas.Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = crud.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article
