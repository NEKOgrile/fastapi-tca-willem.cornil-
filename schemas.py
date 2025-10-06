from sqlmodel import SQLModel, Field
from typing import Optional

class UserCreate(SQLModel):
    username: str
    email: str
    password: str  # mot de passe en clair reçu du client


class UserRead(SQLModel):
    id: int
    username: str
    email: str
    
class UserReadWTF(SQLModel):
    id: int
    username: str
    email: str
    motsWTF: Optional[str] = None
    
class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None  # mot de passe en clair reçu du client
    mots : Optional[str] = None
    
class UserInDB(SQLModel):
    id: int
    username: str
    email: str
    hashed_password: str  # mot de passe haché stocké en DB
    mots : Optional[str] = None
    
class UserDelete(SQLModel):
    id: int
    username: str
    email: str
    mots : Optional[str] = None
    
    