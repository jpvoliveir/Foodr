import pytest
from unittest.mock import MagicMock
from app.services.recommender import recommend_foods


def make_food(id, name, protein, carbs, fat, is_vegan=False, is_vegetarian=False):
    food = MagicMock()
    food.id = id
    food.name = name
    food.protein = protein
    food.carbohydrates = carbs
    food.fat = fat
    food.is_vegan = is_vegan
    food.is_vegetarian = is_vegetarian
    return food


FOODS = [
    make_food(1, "Frango",    31.0,  0.0,  3.6),
    make_food(2, "Arroz",      2.7, 28.0,  0.3),
    make_food(3, "Azeite",     0.0,  0.0, 14.0),
    make_food(4, "Lentilha",   9.0, 20.0,  0.4, is_vegan=True, is_vegetarian=True),
    make_food(5, "Brocolis",   2.8,  7.0,  0.4, is_vegan=True, is_vegetarian=True),
]


def test_returns_correct_limit():
    recs = recommend_foods(140, 250, 58, FOODS, limit=2)
    assert len(recs) == 2


def test_sorted_by_similarity_descending():
    recs = recommend_foods(140, 250, 58, FOODS)
    scores = [r["similarity_score"] for r in recs]
    assert scores == sorted(scores, reverse=True)


def test_vegan_filter_excludes_non_vegan():
    recs = recommend_foods(10, 20, 5, FOODS, diet_preference="vegan")
    names = [r["food"].name for r in recs]
    assert "Frango" not in names
    assert "Arroz" not in names
    assert "Azeite" not in names


def test_vegetarian_filter_allows_vegan_foods():
    recs = recommend_foods(10, 20, 5, FOODS, diet_preference="vegetarian")
    names = [r["food"].name for r in recs]
    assert "Lentilha" in names
    assert "Brocolis" in names


def test_empty_foods_returns_empty():
    recs = recommend_foods(100, 200, 50, [], limit=5)
    assert recs == []


def test_all_zero_macros_food_is_handled():
    zero_food = make_food(99, "Zero", 0.0, 0.0, 0.0)
    recs = recommend_foods(10, 20, 5, [zero_food])
    assert len(recs) == 1
    assert recs[0]["similarity_score"] == 0.0


def test_high_protein_target_favors_protein_rich_food():
    recs = recommend_foods(target_protein=200, target_carbs=10, target_fat=5, foods=FOODS)
    assert recs[0]["food"].name == "Frango"
