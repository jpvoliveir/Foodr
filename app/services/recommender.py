import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
from app.models.food import Food


def recommend_foods(
    target_protein: float,
    target_carbs: float,
    target_fat: float,
    target_calories: float,
    foods: List[Food],
    limit: int = 10
) -> List[Dict[str, Any]]:
    if not foods:
        return []

    # Macro ratio vector for the user's daily target
    user_vector = np.array([[target_protein, target_carbs, target_fat]], dtype=float)
    user_sum = user_vector.sum()
    user_ratio = user_vector / user_sum if user_sum > 0 else user_vector

    # Macro ratio vectors for each food
    food_vectors = []
    for food in foods:
        total = food.protein + food.carbohydrates + food.fat
        if total > 0:
            food_vectors.append([food.protein / total, food.carbohydrates / total, food.fat / total])
        else:
            food_vectors.append([0.0, 0.0, 0.0])

    food_matrix = np.array(food_vectors, dtype=float)
    macro_scores = cosine_similarity(user_ratio, food_matrix)[0]

    # Calorie proximity score: peaks at 1.0 when food matches one meal's worth of calories
    meal_calories = target_calories / 3.0
    recommendations = []
    for idx, food in enumerate(foods):
        macro_score = float(macro_scores[idx])
        if meal_calories > 0:
            calorie_ratio = food.calories / meal_calories
            calorie_score = max(0.0, 1.0 - abs(calorie_ratio - 1.0))
        else:
            calorie_score = 0.0
        combined_score = round(0.7 * macro_score + 0.3 * calorie_score, 4)
        recommendations.append({"food": food, "similarity_score": combined_score})

    recommendations.sort(key=lambda x: x["similarity_score"], reverse=True)
    return recommendations[:limit]
