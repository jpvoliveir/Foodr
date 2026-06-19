from contextlib import asynccontextmanager
import csv
import os
from fastapi import FastAPI
from app.database import engine, Base, SessionLocal
from app.models.food import Food
from app.routes import users, recommendations

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Seed database with foods if empty
    db = SessionLocal()
    try:
        if db.query(Food).count() == 0:
            csv_path = "data/foods.csv"
            if os.path.exists(csv_path):
                with open(csv_path, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        food = Food(
                            id=int(row["id"]),
                            name=row["name"],
                            category=row["category"],
                            calories=float(row["calories"]),
                            protein=float(row["protein"]),
                            carbohydrates=float(row["carbohydrates"]),
                            fat=float(row["fat"]),
                            is_vegetarian=bool(int(row["is_vegetarian"])),
                            is_vegan=bool(int(row["is_vegan"])),
                            is_gluten_free=bool(int(row["is_gluten_free"]))
                        )
                        db.add(food)
                    db.commit()
                    print("Banco de dados populado com sucesso a partir de data/foods.csv!")
            else:
                print(f"Aviso: {csv_path} nao encontrado. O banco nao foi populado.")
    finally:
        db.close()
    
    yield

app = FastAPI(
    title="ML Food Recommender API",
    description="API para calculo metabolico e recomendacao personalizada de alimentos usando Machine Learning.",
    version="1.0.0",
    lifespan=lifespan
)

# Registra os roteadores
app.include_router(users.router)
app.include_router(recommendations.router)

@app.get("/")
def read_root():
    return {
        "status": "running",
        "service": "ML Food Recommender API",
        "docs_url": "/docs"
    }
