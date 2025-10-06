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
    mots: Optional[str] = None

    
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
    

#categories schemas
#ici on vas avoir le groupe de transport (bus, metro, tramway)
#exemple : {"id" : 1 , "'name" : "Métro"}

#creation 
class CategoryCreate(SQLModel):
    name: str

#lecture
class CategoryRead(SQLModel):
    id: int
    name: str

#mise a jour
class CategoryUpdate(SQLModel):
    name: Optional[str] = None

#suppression  
class CategoryDelete(SQLModel):
    id: int
    name: str

#transport line schemas
#ici on va avoir les informations sur les lignes de transport
#exemple : {"id" : 1 , "'name" : "Métro B" , "category_id" : 1 , created_at : "2023-10-10 10:10:10" , start_time : "2023-10-10 10:10:10" , end_time : "2023-10-10 10:10:10"}


#creation
class TransportLineCreate(SQLModel):
    name: str
    category_id: int
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    
#lecture    
class TransportLineRead(SQLModel):
    id: int
    name: str
    category_id: int
    created_at: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

#mise a jour   
class TransportLineUpdate(SQLModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    
#suppression
class TransportLineDelete(SQLModel):
    id: int
    name: str
    category_id: int
    created_at: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None



#stop schemas
#ici on va avoir les informations sur les point geographgique sur arrêts de transport
#exemple : {"id" : 1 , line_id : 5 , "'name" : "Gare de Lyon" , "latitude" : 48.8443 , "longitude" : 2.3730 , stop_order : 1}

#creation
class StopCreate(SQLModel):
    line_id: int
    name: str
    latitude: float
    longitude: float
    stop_order: int

#lecture
class StopRead(SQLModel):
    id: int
    line_id: int
    name: str
    latitude: float
    longitude: float
    stop_order: int
    
#mise a jour
class StopUpdate(SQLModel):
    line_id: Optional[int] = None
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    stop_order: Optional[int] = None
    
#suppression
class StopDelete(SQLModel):
    id: int
    line_id: int
    name: str
    latitude: float
    longitude: float
    stop_order: int