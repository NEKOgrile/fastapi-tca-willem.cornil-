# database.py
import json
from sqlmodel import SQLModel, create_engine, Session

# Charger les identifiants depuis identifiant.json
with open("identifiant.json") as f:
    config = json.load(f)

user = config["user"]
password = config["password"]
host = config["host"]
port = config["port"]
database = config["database"]

# Construire l'URL de connexion
DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Fonction pour créer une session
def get_session():
    with Session(engine) as session:
        yield session
