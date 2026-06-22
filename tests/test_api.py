import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Payload helpers ────────────────────────────────────────────────────────────

USER_PAYLOAD = {
    "name": "João Teste",
    "weight": 75.0,
    "height": 178.0,
    "age": 28,
    "gender": "male",
    "activity_level": "moderate",
    "goal": "lose",
    "diet_preference": "any",
    "gluten_free_preference": False,
}

FOOD_PAYLOAD = {
    "name": "Frango Grelhado",
    "category": "Proteins",
    "calories": 165.0,
    "protein": 31.0,
    "carbohydrates": 0.0,
    "fat": 3.6,
    "is_vegetarian": False,
    "is_vegan": False,
    "is_gluten_free": True,
}

VEGAN_FOOD_PAYLOAD = {
    "name": "Lentilha",
    "category": "Legumes",
    "calories": 116.0,
    "protein": 9.0,
    "carbohydrates": 20.0,
    "fat": 0.4,
    "is_vegetarian": True,
    "is_vegan": True,
    "is_gluten_free": True,
}


# ── Root ───────────────────────────────────────────────────────────────────────

def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "running"


# ── Users ─────────────────────────────────────────────────────────────────────

def test_create_user(client):
    r = client.post("/users/", json=USER_PAYLOAD)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == USER_PAYLOAD["name"]
    assert data["id"] == 1
    assert data["gluten_free_preference"] == False


def test_get_user(client):
    client.post("/users/", json=USER_PAYLOAD)
    r = client.get("/users/1")
    assert r.status_code == 200
    body = r.json()
    assert body["profile"]["name"] == USER_PAYLOAD["name"]
    assert "metabolism_targets" in body


def test_get_user_not_found(client):
    r = client.get("/users/999")
    assert r.status_code == 404


def test_update_user(client):
    client.post("/users/", json=USER_PAYLOAD)
    r = client.put("/users/1", json={"goal": "gain", "weight": 80.0})
    assert r.status_code == 200
    data = r.json()
    assert data["goal"] == "gain"
    assert data["weight"] == 80.0


def test_update_user_gluten_free(client):
    client.post("/users/", json=USER_PAYLOAD)
    r = client.put("/users/1", json={"gluten_free_preference": True})
    assert r.status_code == 200
    assert r.json()["gluten_free_preference"] == True


def test_update_user_not_found(client):
    r = client.put("/users/999", json={"goal": "gain"})
    assert r.status_code == 404


def test_create_user_invalid_gender(client):
    payload = {**USER_PAYLOAD, "gender": "other"}
    r = client.post("/users/", json=payload)
    assert r.status_code == 422


# ── Foods ─────────────────────────────────────────────────────────────────────

def test_create_food(client):
    r = client.post("/foods/", json=FOOD_PAYLOAD)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == FOOD_PAYLOAD["name"]
    assert data["id"] == 1


def test_list_foods_empty(client):
    r = client.get("/foods/")
    assert r.status_code == 200
    assert r.json() == []


def test_list_foods(client):
    client.post("/foods/", json=FOOD_PAYLOAD)
    r = client.get("/foods/")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_list_foods_pagination(client):
    client.post("/foods/", json=FOOD_PAYLOAD)
    client.post("/foods/", json={**FOOD_PAYLOAD, "name": "Arroz"})
    r = client.get("/foods/?skip=1&limit=1")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["name"] == "Arroz"


def test_get_food(client):
    client.post("/foods/", json=FOOD_PAYLOAD)
    r = client.get("/foods/1")
    assert r.status_code == 200
    assert r.json()["name"] == FOOD_PAYLOAD["name"]


def test_get_food_not_found(client):
    r = client.get("/foods/999")
    assert r.status_code == 404


def test_create_food_invalid_calories(client):
    payload = {**FOOD_PAYLOAD, "calories": -10.0}
    r = client.post("/foods/", json=payload)
    assert r.status_code == 422


# ── Recommendations ───────────────────────────────────────────────────────────

def test_recommendations_for_user(client):
    client.post("/users/", json=USER_PAYLOAD)
    client.post("/foods/", json=FOOD_PAYLOAD)
    r = client.get("/recommendations/1")
    assert r.status_code == 200
    body = r.json()
    assert "metabolism_targets" in body
    assert "recommendations" in body
    assert len(body["recommendations"]) == 1


def test_recommendations_user_not_found(client):
    r = client.get("/recommendations/999")
    assert r.status_code == 404


def test_recommendations_no_foods(client):
    client.post("/users/", json=USER_PAYLOAD)
    r = client.get("/recommendations/1")
    assert r.status_code == 400


def test_recommendations_vegan_filter(client):
    vegan_user = {**USER_PAYLOAD, "diet_preference": "vegan"}
    client.post("/users/", json=vegan_user)
    client.post("/foods/", json=FOOD_PAYLOAD)       # não-vegano
    client.post("/foods/", json=VEGAN_FOOD_PAYLOAD) # vegano
    r = client.get("/recommendations/1")
    assert r.status_code == 200
    names = [item["food"]["name"] for item in r.json()["recommendations"]]
    assert "Frango Grelhado" not in names
    assert "Lentilha" in names


def test_recommendations_gluten_free_filter(client):
    gf_user = {**USER_PAYLOAD, "gluten_free_preference": True}
    client.post("/users/", json=gf_user)
    client.post("/foods/", json={**FOOD_PAYLOAD, "is_gluten_free": False, "name": "Pão"})
    client.post("/foods/", json=VEGAN_FOOD_PAYLOAD)  # is_gluten_free=True
    r = client.get("/recommendations/1")
    assert r.status_code == 200
    names = [item["food"]["name"] for item in r.json()["recommendations"]]
    assert "Pão" not in names
    assert "Lentilha" in names


def test_direct_recommendations(client):
    client.post("/foods/", json=FOOD_PAYLOAD)
    r = client.get(
        "/recommendations/direct/run",
        params={
            "weight": 70, "height": 175, "age": 25,
            "gender": "male", "activity_level": "moderate",
            "goal": "lose", "diet_preference": "any", "limit": 5,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert "recommendations" in body
    assert len(body["recommendations"]) == 1


def test_direct_recommendations_gluten_free(client):
    client.post("/foods/", json={**FOOD_PAYLOAD, "is_gluten_free": False, "name": "Pão"})
    client.post("/foods/", json=VEGAN_FOOD_PAYLOAD)
    r = client.get(
        "/recommendations/direct/run",
        params={
            "weight": 70, "height": 175, "age": 25,
            "gender": "male", "activity_level": "moderate",
            "goal": "lose", "gluten_free": True,
        },
    )
    assert r.status_code == 200
    names = [item["food"]["name"] for item in r.json()["recommendations"]]
    assert "Pão" not in names
    assert "Lentilha" in names
