from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.food import Food
from app.schemas.food import FoodCreate, FoodResponse

router = APIRouter(prefix="/foods", tags=["foods"])


@router.post("/", response_model=FoodResponse, status_code=201)
def create_food(food: FoodCreate, db: Session = Depends(get_db)):
    db_food = Food(**food.model_dump())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food


@router.get("/", response_model=list[FoodResponse])
def list_foods(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    return db.query(Food).offset(skip).limit(limit).all()


@router.get("/{food_id}", response_model=FoodResponse)
def get_food(food_id: int, db: Session = Depends(get_db)):
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    return food
