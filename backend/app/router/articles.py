from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app import crud, schemas, models
from app.db import get_db

router = APIRouter(prefix="/articles", tags=["articles"])

@router.post("/", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, author_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.create_article(db=db, article=article, author_id=author_id)

@router.get("/", response_model=List[schemas.Article])
def read_articles(
    skip: int = 0, 
    limit: int = 100, 
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_articles(db, skip=skip, limit=limit, category=category)

@router.get("/{article_id}", response_model=schemas.Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = crud.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article
