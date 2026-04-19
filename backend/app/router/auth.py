from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, schemas, security
from app.db import get_db
from datetime import timedelta
from typing import List


router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "role": user.role,
        "name": user.name,
        "id": user.id,
        "email": user.email
    }

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print(f"DEBUG BACKEND: Received token starting with: {token[:10]}..." if token else "DEBUG BACKEND: No token received")
    try:
        payload = security.decode_access_token(token)
        print(f"DEBUG BACKEND: Decoded payload: {payload}")
        email: str = payload.get("sub")
        if email is None:
            print("DEBUG BACKEND: 'sub' missing from payload")
            raise credentials_exception
    except Exception as e:
        print(f"DEBUG BACKEND: JWT Decode Error: {e}")
        raise credentials_exception
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        print(f"DEBUG BACKEND: User with email {email} not found in DB")
        raise credentials_exception
    return user

async def get_current_active_admin(current_user: schemas.User = Depends(get_current_user)):
    role_value = getattr(current_user.role, "value", current_user.role)
    if role_value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="The user does not have enough privileges"
        )
    return current_user

@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=schemas.User)
async def update_users_me(user_update: schemas.UserSelfUpdate, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, current_user.id, user_update, allow_role=False)
    return updated_user

@router.post("/me/change-password")
async def change_password(passwords: schemas.PasswordChange, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not security.verify_password(passwords.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Mật khẩu cũ không chính xác")
    crud.update_user_password(db, current_user.id, passwords.new_password)
    return {"message": "Đổi mật khẩu thành công"}

@router.get("/me/activities", response_model=List[schemas.UserActivity])
async def read_user_activities(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_user_activities(db, current_user.id)

# Administrative Routes
@router.get("/users", response_model=List[schemas.User])
async def read_users(
    skip: int = 0, 
    limit: int = 100, 
    admin: schemas.User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/count")
async def get_users_count(
    admin: schemas.User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    """Lấy tổng số lượng người dùng (chỉ dành cho Admin)"""
    return {"total": crud.count_users(db)}

@router.delete("/users/{user_id}")
async def remove_user(
    user_id: int, 
    admin: schemas.User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete the current admin account")
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.patch("/users/{user_id}", response_model=schemas.User)
async def update_user_by_admin(
    user_id: int,
    user_update: schemas.UserAdminUpdate,
    admin: schemas.User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    updated_user = crud.update_user(db, user_id, user_update, allow_role=True)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.patch("/users/{user_id}/role", response_model=schemas.User)
async def change_user_role(
    user_id: int,
    role_update: schemas.UserRoleUpdate,
    admin: schemas.User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    if user_id == admin.id and role_update.role != "admin":
        raise HTTPException(status_code=400, detail="Cannot downgrade your own admin role")
    updated_user = crud.update_user(db, user_id, role_update, allow_role=True)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user



