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
    name: str = Field(..., example="Frango Grelhado")
    category: str = Field(..., example="Proteins")
    calories: float = Field(..., gt=0, example=165.0)
    protein: float = Field(..., ge=0, example=31.0)
    carbohydrates: float = Field(..., ge=0, example=0.0)
    fat: float = Field(..., ge=0, example=3.6)
    is_vegetarian: bool = Field(default=False)
    is_vegan: bool = Field(default=False)
    is_gluten_free: bool = Field(default=False)

class FoodCreate(FoodBase):
    pass

class FoodResponse(FoodBase):
    id: int

    model_config = {
        "from_attributes": True
    }
