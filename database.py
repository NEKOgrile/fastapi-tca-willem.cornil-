# database.py
from sqlmodel import SQLModel, create_engine, Session

# Connexion à la base MariaDB locale
DATABASE_URL = "mysql+mysqlconnector://root:E5EAAC93E5@127.0.0.1:3306/project_API_TISSEA"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Fonction pour créer une session
def get_session():
    with Session(engine) as session:
        yield session
