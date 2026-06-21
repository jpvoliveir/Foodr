import pytest
from app.services.metabolism import calculate_metabolism


def test_bmr_male():
    result = calculate_metabolism(
        weight=80, height=180, age=25,
        gender="male", activity_level="sedentary", goal="maintain"
    )
    # Mifflin-St Jeor: 10*80 + 6.25*180 - 5*25 + 5 = 1805
    assert result["bmr"] == 1805.0


def test_bmr_female():
    result = calculate_metabolism(
        weight=60, height=165, age=30,
        gender="female", activity_level="sedentary", goal="maintain"
    )
    # 10*60 + 6.25*165 - 5*30 - 161 = 1320.25 → rounded to 1320.2
    assert result["bmr"] == 1320.2


def test_tdee_moderate_activity():
    result = calculate_metabolism(
        weight=70, height=175, age=25,
        gender="male", activity_level="moderate", goal="maintain"
    )
    bmr = 10 * 70 + 6.25 * 175 - 5 * 25 + 5
    assert result["tdee"] == round(bmr * 1.55, 1)


def test_goal_lose_subtracts_500():
    result = calculate_metabolism(
        weight=70, height=175, age=25,
        gender="male", activity_level="moderate", goal="lose"
    )
    result_maintain = calculate_metabolism(
        weight=70, height=175, age=25,
        gender="male", activity_level="moderate", goal="maintain"
    )
    assert result["target_calories"] == result_maintain["target_calories"] - 500


def test_goal_gain_adds_500():
    result = calculate_metabolism(
        weight=70, height=175, age=25,
        gender="male", activity_level="moderate", goal="gain"
    )
    result_maintain = calculate_metabolism(
        weight=70, height=175, age=25,
        gender="male", activity_level="moderate", goal="maintain"
    )
    assert result["target_calories"] == result_maintain["target_calories"] + 500


def test_minimum_calories_floor():
    # Very light person to trigger the 1200 kcal floor
    result = calculate_metabolism(
        weight=30, height=150, age=60,
        gender="female", activity_level="sedentary", goal="lose"
    )
    assert result["target_calories"] >= 1200.0


def test_macros_sum_to_target_calories():
    result = calculate_metabolism(
        weight=75, height=178, age=28,
        gender="male", activity_level="active", goal="maintain"
    )
    protein_kcal = result["target_protein_g"] * 4
    carb_kcal = result["target_carbs_g"] * 4
    fat_kcal = result["target_fat_g"] * 9
    total = protein_kcal + carb_kcal + fat_kcal
    assert abs(total - result["target_calories"]) < 1.0
