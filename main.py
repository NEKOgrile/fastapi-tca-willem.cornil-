# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session
from database import engine, get_session
from models import *        # ➜ User de la base de données (DB)
from schemas.schemas import *
from jwt import authenticate_user, create_access_token, get_current_user, fake_users_db

import hashlib  # pour hasher le mot de passe (à remplacer par bcrypt en prod)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

#------------------------------------------------------------------------------
# Authentification fake JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    user = fake_users_db.get(username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
#------------------------------------------------------------------------------

# --- Création des tables à chaque démarrage si elles n'existent pas ---
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

#------------------------------------------------------------------------------
# Endpoints pour la gestion des utilisateurs
#------------------------------------------------------------------------------

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



#----------------------------------------------------------------------
# Ici on vas faire les endpoints pour les categories , les lignes de transport et les arrets
#----------------------------------------------------------------------

# --- Endpoints pour la creation de transport ---
@app.post("/api/creat/category" , response_model=CategoryRead)
def create_category(category_api: CategoryCreate, session: Session = Depends(get_session)):
    db_category = categories(
        name=category_api.name
    )
    
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    
    
    return db_category


# --- Endpoints pour la lecture de transport ---
@app.get("/api/category/{category_id}" , response_model=CategoryRead)
def get_category(category_id: int, session: Session = Depends(get_session)):
    db_category = session.get(categories, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    return db_category


# --- Endpoints pour la mise a jour de transport ---
@app.put("/api/update/category/{category_id}" , response_model=CategoryUpdate)
def update_category(category_id: int, category_update: CategoryUpdate, session: Session = Depends(get_session)):
    db_category = session.get(categories, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    
    if category_update.name is not None:
        existing_category_name = session.query(categories).filter(categories.name == category_update.name, categories.id != category_id).first()
        if existing_category_name:
            raise HTTPException(status_code=400, detail="le nom est déjà utilisé")
        db_category.name = category_update.name
        
    category_api = CategoryUpdate(
        name=db_category.name
    )
    
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    
    return category_api


# --- Endpoints pour la suppression de transport ---
@app.delete("/api/delete/category/{category_id}" , response_model=CategoryDelete)
def delete_category(category_id: int, session: Session = Depends(get_session)):
    db_category = session.get(categories, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    
    category_api = CategoryDelete(
        id=db_category.id,
        name=db_category.name
    )
    
    session.delete(db_category)
    session.commit()
    
    return category_api


# --- Endpoints pour la lecture de toutes les categories ---
@app.get("/api/allcategory" , response_model=list[CategoryRead])
def get_all_category(session: Session = Depends(get_session)):
    category = session.query(categories).all()
    return category

#------------------------------------------------------------------------------
# Endpoints pour la gestion des lignes de transport
#------------------------------------------------------------------------------

# --- Endpoints pour la creation de transport line ---
@app.post("/api/creat/line" , response_model=TransportLineRead)
def create_transport_line(line_api: TransportLineCreate, session: Session = Depends(get_session)):
    # Vérifier si la catégorie existe
    db_category = session.get(categories, line_api.category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    
    db_line = TransportLine( 
        name=line_api.name,
        category_id=line_api.category_id,
        start_time=line_api.start_time if line_api.start_time else time(5, 0),
        end_time=line_api.end_time if line_api.end_time else time(23, 0)
    )
    
    session.add(db_line)
    session.commit()
    session.refresh(db_line)
    
    return db_line

# --- Endpoints pour la lecture de transport line ---
@app.get("/api/line/{line_id}" , response_model=TransportLineRead)
def get_transport_line(line_id: int, session: Session = Depends(get_session)):
    db_line = session.get(TransportLine, line_id)
    if not db_line:
        raise HTTPException(status_code=404, detail="Ligne non trouvée")
    return db_line


# --- Endpoints pour la mise a jour de transport line ---
@app.put("/api/update/line/{line_id}" , response_model=TransportLineUpdate)
def update_transport_line(line_id: int, line_update: TransportLineUpdate, session: Session = Depends(get_session)):
    db_line = session.get(TransportLine, line_id)
    if not db_line:
        raise HTTPException(status_code=404, detail="Ligne non trouvée")
    
    if line_update.name is not None:
        existing_line_name = session.query(TransportLine).filter(TransportLine.name == line_update.name, TransportLine.id != line_id).first()
        if existing_line_name:
            raise HTTPException(status_code=400, detail="le nom est déjà utilisé")
        db_line.name = line_update.name
        
    if line_update.category_id is not None:
        # Vérifier si la nouvelle catégorie existe
        db_category = session.get(categories, line_update.category_id)
        if not db_category:
            raise HTTPException(status_code=404, detail="Catégorie non trouvée")
        db_line.category_id = line_update.category_id
        
    if line_update.start_time is not None:
        db_line.start_time = line_update.start_time
        
    if line_update.end_time is not None:
        db_line.end_time = line_update.end_time
        
    line_api = TransportLineUpdate(
        name=db_line.name,
        category_id=db_line.category_id,
        start_time=db_line.start_time,
        end_time=db_line.end_time
    )
    
    session.add(db_line)
    session.commit()
    session.refresh(db_line)
    
    return line_api

# --- Endpoints pour la suppression de transport line ---
@app.delete("/api/delete/line/{line_id}" , response_model=TransportLineDelete)
def delete_transport_line(line_id: int, session: Session = Depends(get_session)):
    db_line = session.get(TransportLine, line_id)
    if not db_line:
        raise HTTPException(status_code=404, detail="Ligne non trouvée")
    
    line_api = TransportLineDelete(
        id=db_line.id,
        name=db_line.name,
        category_id=db_line.category_id,
        created_at=db_line.created_at,
        start_time=db_line.start_time,
        end_time=db_line.end_time
    )
    
    session.delete(db_line)
    session.commit()
    
    return line_api

# --- Endpoints pour la lecture de toutes les lignes de transport ---
@app.get("/api/allline" , response_model=list[TransportLineRead])
def get_all_transport_lines(session: Session = Depends(get_session)):
    lines = session.query(TransportLine).all()
    return lines


#------------------------------------------------------------------------------
# Endpoints pour la gestion des arrêts
#------------------------------------------------------------------------------

# --- Endpoints pour la creation d'arrêt ---
@app.post("/api/creat/stop" , response_model=StopRead)
def create_stop(stop_api: StopCreate, session: Session = Depends(get_session)):
    # Vérifier si la ligne de transport existe
    db_line = session.get(TransportLine, stop_api.line_id)
    if not db_line:
        raise HTTPException(status_code=404, detail="Ligne de transport non trouvée")
    
    db_stop = Stop(
        line_id=stop_api.line_id,
        name=stop_api.name,
        latitude=stop_api.latitude,
        longitude=stop_api.longitude,
        stop_order=stop_api.stop_order
    )
    
    session.add(db_stop)
    session.commit()
    session.refresh(db_stop)
    
    return db_stop


# --- Endpoints pour la lecture d'arrêt ---
@app.get("/api/stop/{stop_id}" , response_model=StopRead)
def get_stop(stop_id: int, session: Session = Depends(get_session)):
    db_stop = session.get(Stop, stop_id)
    if not db_stop:
        raise HTTPException(status_code=404, detail="Arrêt non trouvé")
    return db_stop

# --- Endpoints pour la mise a jour d'arrêt ---
@app.put("/api/update/stop/{stop_id}" , response_model=StopUpdate)
def update_stop(stop_id: int, stop_update: StopUpdate, session: Session = Depends(get_session)):
    db_stop = session.get(Stop, stop_id)
    if not db_stop:
        raise HTTPException(status_code=404, detail="Arrêt non trouvé")
    
    if stop_update.line_id is not None:
        # Vérifier si la nouvelle ligne de transport existe
        db_line = session.get(TransportLine, stop_update.line_id)
        if not db_line:
            raise HTTPException(status_code=404, detail="Ligne de transport non trouvée")
        db_stop.line_id = stop_update.line_id
        
    if stop_update.name is not None:
        db_stop.name = stop_update.name
        
    if stop_update.latitude is not None:
        db_stop.latitude = stop_update.latitude
        
    if stop_update.longitude is not None:
        db_stop.longitude = stop_update.longitude
        
    if stop_update.stop_order is not None:
        db_stop.stop_order = stop_update.stop_order
        
    stop_api = StopUpdate(
        line_id=db_stop.line_id,
        name=db_stop.name,
        latitude=db_stop.latitude,
        longitude=db_stop.longitude,
        stop_order=db_stop.stop_order
    )
    
    session.add(db_stop)
    session.commit()
    session.refresh(db_stop)
    
    return stop_api

# --- Endpoints pour la suppression d'arrêt ---
@app.delete("/api/delete/stop/{stop_id}" , response_model=StopRead)
def delete_stop(stop_id: int, session: Session = Depends(get_session)):
    db_stop = session.get(Stop, stop_id)
    if not db_stop:
        raise HTTPException(status_code=404, detail="Arrêt non trouvé")
    
    stop_api = StopRead(
        id=db_stop.id,
        line_id=db_stop.line_id,
        name=db_stop.name,
        latitude=db_stop.latitude,
        longitude=db_stop.longitude,
        stop_order=db_stop.stop_order
    )
    
    session.delete(db_stop)
    session.commit()
    
    return stop_api

# --- Endpoints pour la lecture de tous les arrêts ---
@app.get("/api/allstop" , response_model=list[StopRead])
def get_all_stops(session: Session = Depends(get_session)):
    stops = session.query(Stop).all()
    return stops
