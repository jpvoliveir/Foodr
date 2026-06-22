from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    weight = Column(Float)
    height = Column(Float)
    age = Column(Integer)
    gender = Column(String)
    activity_level = Column(String)
    goal = Column(String)
    diet_preference = Column(String)
    gluten_free_preference = Column(Boolean, default=False)
