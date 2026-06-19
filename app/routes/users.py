from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserCreate, UserResponse, UserUpdate
from app.services.metabolism import calculate_metabolism

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=210)  # Standard status code or 201
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Create the database record using pydantic model dump
    db_user = User(
        name=user.name,
        weight=user.weight,
        height=user.height,
        age=user.age,
        gender=user.gender,
        activity_level=user.activity_level,
        goal=user.goal,
        diet_preference=user.diet_preference
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Calculate metabolism targets
    targets = calculate_metabolism(
        weight=db_user.weight,
        height=db_user.height,
        age=db_user.age,
        gender=db_user.gender,
        activity_level=db_user.activity_level,
        goal=db_user.goal
    )
    
    return {
        "profile": UserResponse.model_validate(db_user),
        "metabolism_targets": targets
    }

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.commit()
    db.refresh(db_user)
    return db_user
