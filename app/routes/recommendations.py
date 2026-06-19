from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.models.food import Food, FoodResponse
from app.services.metabolism import calculate_metabolism
from app.services.recommender import recommend_foods

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/{user_id}")
def get_recommendations_for_user(
    user_id: int,
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    # 1. Fetch user from DB
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # 2. Calculate daily targets
    targets = calculate_metabolism(
        weight=db_user.weight,
        height=db_user.height,
        age=db_user.age,
        gender=db_user.gender,
        activity_level=db_user.activity_level,
        goal=db_user.goal
    )

    # 3. Get all foods
    foods = db.query(Food).all()
    if not foods:
        raise HTTPException(status_code=400, detail="Nenhum alimento cadastrado no banco de dados")

    # 4. Generate recommendations
    recs = recommend_foods(
        target_protein=targets["target_protein_g"],
        target_carbs=targets["target_carbs_g"],
        target_fat=targets["target_fat_g"],
        foods=foods,
        diet_preference=db_user.diet_preference,
        limit=limit
    )

    # 5. Format output
    formatted_recs = []
    for r in recs:
        formatted_recs.append({
            "food": FoodResponse.model_validate(r["food"]),
            "similarity_score": r["similarity_score"]
        })

    return {
        "user_id": user_id,
        "metabolism_targets": targets,
        "recommendations": formatted_recs
    }

@router.get("/direct/run")  # Can be /direct
def get_direct_recommendations(
    weight: float = Query(..., gt=0, description="Peso em kg"),
    height: float = Query(..., gt=0, description="Altura em cm"),
    age: int = Query(..., gt=0, description="Idade em anos"),
    gender: str = Query(..., regex="^(male|female)$"),
    activity_level: str = Query(..., regex="^(sedentary|light|moderate|active|very_active)$"),
    goal: str = Query(..., regex="^(lose|maintain|gain)$"),
    diet_preference: str = Query(default="any", regex="^(any|vegetarian|vegan)$"),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    # 1. Calculate daily targets on the fly
    targets = calculate_metabolism(
        weight=weight,
        height=height,
        age=age,
        gender=gender,
        activity_level=activity_level,
        goal=goal
    )

    # 2. Get all foods
    foods = db.query(Food).all()
    if not foods:
        raise HTTPException(status_code=400, detail="Nenhum alimento cadastrado no banco de dados")

    # 3. Generate recommendations
    recs = recommend_foods(
        target_protein=targets["target_protein_g"],
        target_carbs=targets["target_carbs_g"],
        target_fat=targets["target_fat_g"],
        foods=foods,
        diet_preference=diet_preference,
        limit=limit
    )

    # 4. Format output
    formatted_recs = []
    for r in recs:
        formatted_recs.append({
            "food": FoodResponse.model_validate(r["food"]),
            "similarity_score": r["similarity_score"]
        })

    return {
        "metabolism_targets": targets,
        "recommendations": formatted_recs
    }
