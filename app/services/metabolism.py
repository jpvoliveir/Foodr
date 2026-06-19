ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9
}

def calculate_metabolism(
    weight: float,
    height: float,
    age: int,
    gender: str,
    activity_level: str,
    goal: str
) -> dict:
    # 1. Calculate BMR (Mifflin-St Jeor Equation)
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # 2. Calculate TDEE
    activity_multiplier = ACTIVITY_MULTIPLIERS.get(activity_level.lower(), 1.2)
    tdee = bmr * activity_multiplier

    # 3. Calculate target calories based on goal
    if goal.lower() == "lose":
        target_calories = tdee - 500
    elif goal.lower() == "gain":
        target_calories = tdee + 500
    else:
        target_calories = tdee

    # Ensure target calories do not drop below a healthy minimum (e.g., 1200 kcal)
    target_calories = max(target_calories, 1200.0)

    # 4. Calculate Macronutrient Targets
    # Protein: 2g/kg of body weight (4 kcal/g)
    protein_g = weight * 2.0
    protein_kcal = protein_g * 4.0

    # If protein calories exceed 35% of total target calories, cap it at 30% of total target calories
    if protein_kcal > (target_calories * 0.35):
        protein_kcal = target_calories * 0.30
        protein_g = protein_kcal / 4.0

    # Fat: 25% of total target calories (9 kcal/g)
    fat_kcal = target_calories * 0.25
    fat_g = fat_kcal / 9.0

    # Carbohydrates: The remaining calories (4 kcal/g)
    carb_kcal = target_calories - (protein_kcal + fat_kcal)
    # Ensure carb calories aren't negative (edge case)
    carb_kcal = max(carb_kcal, 0.0)
    carb_g = carb_kcal / 4.0

    return {
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "target_calories": round(target_calories, 1),
        "target_protein_g": round(protein_g, 1),
        "target_carbs_g": round(carb_g, 1),
        "target_fat_g": round(fat_g, 1)
    }
