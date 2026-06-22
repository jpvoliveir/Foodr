from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.food import Food
from app.schemas.food import FoodResponse
from app.schemas.recommendation import (
    MetabolismTargets, RecommendationItem,
    RecommendationResponse, DirectRecommendationResponse
)
from app.services.metabolism import calculate_metabolism
from app.services.recommender import recommend_foods

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def _filter_foods(db: Session, diet_preference: str, gluten_free: bool):
    query = db.query(Food)
    if diet_preference == "vegan":
        query = query.filter(Food.is_vegan == True)
    elif diet_preference == "vegetarian":
        query = query.filter((Food.is_vegetarian == True) | (Food.is_vegan == True))
    if gluten_free:
        query = query.filter(Food.is_gluten_free == True)
    return query.all()


def _format_recs(recs):
    return [
        RecommendationItem(
            food=FoodResponse.model_validate(r["food"]),
            similarity_score=r["similarity_score"]
        )
        for r in recs
    ]


@router.get("/direct/run", response_model=DirectRecommendationResponse)
def get_direct_recommendations(
    weight: float = Query(..., gt=0, description="Peso em kg"),
    height: float = Query(..., gt=0, description="Altura em cm"),
    age: int = Query(..., gt=0, description="Idade em anos"),
    gender: str = Query(..., pattern="^(male|female)$"),
    activity_level: str = Query(..., pattern="^(sedentary|light|moderate|active|very_active)$"),
    goal: str = Query(..., pattern="^(lose|maintain|gain)$"),
    diet_preference: str = Query(default="any", pattern="^(any|vegetarian|vegan)$"),
    gluten_free: bool = Query(default=False),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    targets = calculate_metabolism(
        weight=weight, height=height, age=age,
        gender=gender, activity_level=activity_level, goal=goal
    )

    foods = _filter_foods(db, diet_preference, gluten_free)
    if not foods:
        raise HTTPException(status_code=400, detail="Nenhum alimento cadastrado no banco de dados")

    recs = recommend_foods(
        target_protein=targets["target_protein_g"],
        target_carbs=targets["target_carbs_g"],
        target_fat=targets["target_fat_g"],
        target_calories=targets["target_calories"],
        foods=foods,
        limit=limit
    )

    return DirectRecommendationResponse(
        metabolism_targets=MetabolismTargets(**targets),
        recommendations=_format_recs(recs)
    )


@router.get("/{user_id}", response_model=RecommendationResponse)
def get_recommendations_for_user(
    user_id: int,
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    targets = calculate_metabolism(
        weight=db_user.weight,
        height=db_user.height,
        age=db_user.age,
        gender=db_user.gender,
        activity_level=db_user.activity_level,
        goal=db_user.goal
    )

    foods = _filter_foods(db, db_user.diet_preference, db_user.gluten_free_preference)
    if not foods:
        raise HTTPException(status_code=400, detail="Nenhum alimento cadastrado no banco de dados")

    recs = recommend_foods(
        target_protein=targets["target_protein_g"],
        target_carbs=targets["target_carbs_g"],
        target_fat=targets["target_fat_g"],
        target_calories=targets["target_calories"],
        foods=foods,
        limit=limit
    )

    return RecommendationResponse(
        user_id=user_id,
        metabolism_targets=MetabolismTargets(**targets),
        recommendations=_format_recs(recs)
    )
