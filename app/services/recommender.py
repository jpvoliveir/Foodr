import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
from app.models.food import Food

def recommend_foods(
    target_protein: float,
    target_carbs: float,
    target_fat: float,
    foods: List[Food],
    diet_preference: str = "any",
    limit: int = 10
) -> List[Dict[str, Any]]:
    # 1. Filter foods by diet preference
    filtered_foods = []
    for food in foods:
        if diet_preference == "vegan" and not food.is_vegan:
            continue
        if diet_preference == "vegetarian" and not food.is_vegetarian and not food.is_vegan:
            # A vegan food is also vegetarian
            continue
        filtered_foods.append(food)

    if not filtered_foods:
        return []

    # 2. Build User Target Ratio Vector
    user_vector = np.array([[target_protein, target_carbs, target_fat]], dtype=float)
    user_sum = user_vector.sum()
    user_ratio = user_vector / user_sum if user_sum > 0 else user_vector

    # 3. Build Food Ratio Vectors
    food_vectors = []
    for food in filtered_foods:
        total = food.protein + food.carbohydrates + food.fat
        if total > 0:
            ratio = [food.protein / total, food.carbohydrates / total, food.fat / total]
        else:
            ratio = [0.0, 0.0, 0.0]
        food_vectors.append(ratio)
    
    food_vectors = np.array(food_vectors, dtype=float)

    # 4. Compute Cosine Similarity
    similarities = cosine_similarity(user_ratio, food_vectors)[0]

    # 5. Build and sort recommendations
    recommendations = []
    for idx, food in enumerate(filtered_foods):
        score = float(similarities[idx])
        recommendations.append({
            "food": food,
            "similarity_score": round(score, 4)
        })

    # Sort descending by similarity score
    recommendations.sort(key=lambda x: x["similarity_score"], reverse=True)

    return recommendations[:limit]
