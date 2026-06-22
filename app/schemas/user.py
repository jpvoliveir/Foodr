from pydantic import BaseModel, Field
from typing import Optional


class UserBase(BaseModel):
    name: str = Field(..., example="João Silva")
    weight: float = Field(..., gt=0, example=80.0, description="Peso em kg")
    height: float = Field(..., gt=0, example=180.0, description="Altura em cm")
    age: int = Field(..., gt=0, example=25, description="Idade em anos")
    gender: str = Field(..., pattern="^(male|female)$", example="male")
    activity_level: str = Field(..., pattern="^(sedentary|light|moderate|active|very_active)$", example="moderate")
    goal: str = Field(..., pattern="^(lose|maintain|gain)$", example="lose")
    diet_preference: str = Field(default="any", pattern="^(any|vegetarian|vegan)$", example="any")
    gluten_free_preference: bool = Field(default=False, description="Filtrar apenas alimentos sem glúten")


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    weight: Optional[float] = Field(None, gt=0)
    height: Optional[float] = Field(None, gt=0)
    age: Optional[int] = Field(None, gt=0)
    gender: Optional[str] = Field(None, pattern="^(male|female)$")
    activity_level: Optional[str] = Field(None, pattern="^(sedentary|light|moderate|active|very_active)$")
    goal: Optional[str] = Field(None, pattern="^(lose|maintain|gain)$")
    diet_preference: Optional[str] = Field(None, pattern="^(any|vegetarian|vegan)$")
    gluten_free_preference: Optional[bool] = None


class UserResponse(UserBase):
    id: int

    model_config = {"from_attributes": True}
