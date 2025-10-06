# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session
from database import engine, get_session
from models import Users        # ➜ User de la base de données (DB)
from schemas.schemas import UserCreate, UserRead , UserUpdate , UserDelete , UserInDB # ➜ User de l'API
import hashlib  # pour hasher le mot de passe (à remplacer par bcrypt en prod)

app = FastAPI()

# --- Création des tables à chaque démarrage si elles n'existent pas ---
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# --- Endpoint POST pour créer un utilisateur ---
@app.post("/users", response_model=UserRead)
def create_user(user_api: UserCreate, session: Session = Depends(get_session)):
    """
    user_api : instance de UserCreate (API) avec mot de passe en clair
    db_user : instance de User (DB) avec hashed_password
    """

    # Vérifier si l'email existe déjà dans la DB
    existing_user = session.query(Users).filter(Users.email == user_api.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    # Hacher le mot de passe reçu via l'API
    hashed_pwd = hashlib.sha256(user_api.password.encode()).hexdigest()

    # Créer un utilisateur DB à partir des données de l'API
    db_user = Users(
        username=user_api.username, 
        email=user_api.email, 
        hashed_password=hashed_pwd
    )

    # Ajouter dans la session et commit
    session.add(db_user)
    session.commit()
    session.refresh(db_user)  # recharge l'utilisateur pour récupérer l'ID généré

    # Retourner une réponse API (UserRead) sans mot de passe
    return db_user

# --- Endpoint GET pour récupérer un utilisateur par ID ---
@app.get("/users/{user_id}", response_model=UserRead)
def get_read_user_wtf(user_id: int, session = Depends(get_session)):
    #ici il vas automatiquement cherche l id car il est en clef primaire et si je voulaist chercher
    # par un autre champ je devrais faire une requete filtrée exemple : 
    #user = session.query(User).filter(User.username == "toto").first()
    db_user =  session.get(Users, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # On "transforme" le db_user en schéma UserRead sinon erreur car il manque le champs motsWTF
    # parceque db_user c est la base de donnée et peut etre qu il y a des champ que l on veux pas 
    #parceque on veux pas afficcher tout (exemple le mot de passe) ou parceque on veux ajouter des champs
    # qui n existe pas dans la base de donnée (exemple motsWTF)
    user_api = UserRead(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        motsWTF="Message forcé"
    )
    return user_api

# --- Endpoint PUT pour mettre à jour un utilisateur ---
@app .put("/update/users/{user_id}", response_model=UserUpdate)
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    db_user = session.get(Users, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Mettre à jour les champs si fournis
    if user_update.username is not None:
        existing_user_name = session.query(Users).filter(Users.username == user_update.username, Users.id != user_id).first()
        if existing_user_name:
            raise HTTPException(status_code=400, detail="le nom est déjà utilisé")
        db_user.username = user_update.username
        
    if user_update.email is not None:
        # Vérifier si le nouvel email est déjà utilisé par un autre utilisateur
        existing_user_email = session.query(Users).filter(Users.email == user_update.email, Users.id != user_id).first()
        if existing_user_email:
            raise HTTPException(status_code=400, detail="Email déjà utilisé")
        db_user.email = user_update.email
        
    if user_update.password is not None:
        db_user.hashed_password = hashlib.sha256(user_update.password.encode()).hexdigest() # Hacher le nouveau mot de passe


    user_api = UserUpdate(
        username=db_user.username,
        email=db_user.email,
        password=None,  # Ne pas renvoyer le mot de passe
        mots = "modification réussie" 
    )

    # je met a jour la base de donnée
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return user_api

# --- Endpoint DELETE pour supprimer un utilisateur ---
@app.delete("/delete/users/{user_id}", response_model=UserDelete)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.get(Users, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    user_api = UserDelete(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        mots = "suppression réussie" 
    )

    session.delete(db_user)
    session.commit()

    return user_api

# --- Endpoint GET pour récupérer tous les utilisateurs ---
@app.get("/allusers", response_model=list[UserInDB])
def get_all_users(session: Session = Depends(get_session)):
    users = session.query(Users).all()
    return users
