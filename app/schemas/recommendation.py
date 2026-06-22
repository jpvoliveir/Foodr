from pydantic import BaseModel
from typing import List
from app.schemas.food import FoodResponse
from app.schemas.user import UserResponse


class MetabolismTargets(BaseModel):
    bmr: float
    tdee: float
    target_calories: float
    target_protein_g: float
    target_carbs_g: float
    target_fat_g: float


class RecommendationItem(BaseModel):
    food: FoodResponse
    similarity_score: float


class UserWithMetabolism(BaseModel):
    profile: UserResponse
    metabolism_targets: MetabolismTargets


class RecommendationResponse(BaseModel):
    user_id: int
    metabolism_targets: MetabolismTargets
    recommendations: List[RecommendationItem]


class DirectRecommendationResponse(BaseModel):
    metabolism_targets: MetabolismTargets
    recommendations: List[RecommendationItem]
