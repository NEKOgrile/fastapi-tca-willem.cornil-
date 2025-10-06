from sqlmodel import SQLModel, Field
from typing import Optional

#le nom de la class doit etre le meme que celui de la base de donnée pas pour faire jolie mais parceque sqlmodel va faire le lien entre les deux

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
