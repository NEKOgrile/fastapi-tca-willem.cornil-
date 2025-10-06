from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, time

# -----------------------------
# 🧍 Utilisateurs
# -----------------------------
class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# -----------------------------
# 🚍 Catégories (bus, métro, tramway)
# -----------------------------
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str



# -----------------------------
# 🚇 Lignes de transport
# -----------------------------
class TransportLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category_id: int = Field(foreign_key="category.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    start_time: time = Field(default=time(5, 0))   # 05:00 par défaut
    end_time: time = Field(default=time(23, 0))   # 23:00 par défaut


# -----------------------------
# 🚏 Arrêts
# -----------------------------
class Stop(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    line_id: int = Field(foreign_key="transportline.id")
    name: str
    latitude: float
    longitude: float
    stop_order: int

