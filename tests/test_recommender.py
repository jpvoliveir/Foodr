import pytest
from unittest.mock import MagicMock
from app.services.recommender import recommend_foods


def make_food(id, name, protein, carbs, fat, calories=100.0):
    food = MagicMock()
    food.id = id
    food.name = name
    food.protein = protein
    food.carbohydrates = carbs
    food.fat = fat
    food.calories = calories
    return food


FOODS = [
    make_food(1, "Frango",   31.0,  0.0,  3.6, calories=165.0),
    make_food(2, "Arroz",     2.7, 28.0,  0.3, calories=130.0),
    make_food(3, "Azeite",    0.0,  0.0, 14.0, calories=120.0),
    make_food(4, "Lentilha",  9.0, 20.0,  0.4, calories=116.0),
    make_food(5, "Brocolis",  2.8,  7.0,  0.4, calories=34.0),
]


def test_returns_correct_limit():
    recs = recommend_foods(140, 250, 58, target_calories=2000, foods=FOODS, limit=2)
    assert len(recs) == 2


def test_sorted_by_similarity_descending():
    recs = recommend_foods(140, 250, 58, target_calories=2000, foods=FOODS)
    scores = [r["similarity_score"] for r in recs]
    assert scores == sorted(scores, reverse=True)


def test_empty_foods_returns_empty():
    recs = recommend_foods(100, 200, 50, target_calories=2000, foods=[], limit=5)
    assert recs == []


def test_all_zero_macros_food_is_handled():
    zero_food = make_food(99, "Zero", 0.0, 0.0, 0.0, calories=0.0)
    recs = recommend_foods(10, 20, 5, target_calories=2000, foods=[zero_food])
    assert len(recs) == 1
    assert recs[0]["similarity_score"] == 0.0


def test_high_protein_target_favors_protein_rich_food():
    recs = recommend_foods(200, 10, 5, target_calories=2000, foods=FOODS)
    assert recs[0]["food"].name == "Frango"
