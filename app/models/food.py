from sqlalchemy import Column, Integer, String, Float, Boolean
from pydantic import BaseModel, Field
from app.database import Base

class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    calories = Column(Float)
    protein = Column(Float)
    carbohydrates = Column(Float)
    fat = Column(Float)
    is_vegetarian = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    is_gluten_free = Column(Boolean, default=False)

# Pydantic Schemas
class FoodBase(BaseModel):
    name: str
    category: str
    calories: float
    protein: float
    carbohydrates: float
    fat: float
    is_vegetarian: bool
    is_vegan: bool
    is_gluten_free: bool

class FoodResponse(FoodBase):
    id: int

    model_config = {
        "from_attributes": True
    }
