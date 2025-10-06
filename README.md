# fastapi-tca-willem.cornil-

Projet FastAPI avec MariaDB, gestion des utilisateurs et structure prête pour extension.

---

## 🚀 Aperçu

Ce projet fournit :  
- Un serveur FastAPI prêt à l’emploi  
- Connexion à MariaDB via SQLModel  
- CRUD complet pour les utilisateurs  
- Structure modulaire pour modèles, schémas et routes  
- Documentation interactive via `/docs`

---

## 📦 Dépendances principales

| Librairie       | Description                               | Version Exemple |
|-----------------|-------------------------------------------|----------------|
| FastAPI         | Framework web rapide pour Python          | 0.99.1         |
| Uvicorn         | Serveur ASGI pour exécuter FastAPI        | 0.23.1         |
| SQLModel        | ORM et gestion de modèles SQL             | 0.0.8          |
| PyMySQL         | Connecteur MariaDB/MySQL pour SQLAlchemy  | 1.1.0          |

> Remarque : lors de l’installation, pip prendra la **dernière version disponible**, pas forcément celle indiquée dans le tableau.

---

## 💻 Installation complète (Windows / PowerShell ou Git Bash)

```powershell
# Cloner le repo
git clone https://github.com/NEKOgrile/fastapi-tca-willem.cornil-.git
cd fastapi-tca-willem.cornil-

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows PowerShell
.\venv\Scripts\activate
# Linux / macOS
# source ./venv/bin/activate

# Mettre pip à jour et installer les dépendances
python -m pip install --upgrade pip
pip install fastapi uvicorn sqlmodel pymysql

# Créer le fichier identifiant.json avec un exemple
echo "{ \"user\": \"root\", \"password\": \"mdp\", \"host\": \"127.0.0.1\", \"port\": 3306, \"database\": \"project_API_TISSEA\" }" > identifiant.json

# Lancer le serveur FastAPI
uvicorn main:app --reload
```

---

## 🔑 Gestion des identifiants (identifiant.json)

- Le fichier `identifiant.json` doit être **dans le dossier racine du projet**.  
- Exemple de contenu :

```json
{
    "user": "root",
    "password": "mdp",
    "host": "127.0.0.1",
    "port": 3306,
    "database": "project_API_TISSEA"
}
```

- Si tu changes ton mot de passe ou le nom de la base, **mets à jour ce fichier**.  
- `database.py` lit automatiquement ce fichier pour construire `DATABASE_URL`.

---

## 🌐 Utilisation

- Serveur accessible à : `http://127.0.0.1:8000`  
- Documentation interactive : `http://127.0.0.1:8000/docs`  

---

## 🗂 Structure du projet

```text
fastapi-tca-willem.cornil-/
├─ main.py           # Point d’entrée FastAPI
├─ database.py       # Connexion MariaDB / SQLModel
├─ models/           # Modèles SQLModel
├─ schemas/          # Schémas Pydantic / SQLModel
├─ routers/          # Endpoints regroupés par thème
├─ venv/             # Environnement virtuel (ignoré par Git)
├─ __pycache__/      # Cache Python (ignoré par Git)
└─ node_modules/     # Optionnel (ignoré par Git)
```

---

## ⚡ Notes importantes

1. Mettre à jour `identifiant.json` si vos informations de base changent.  
2. Pour ajouter d’autres dépendances :  

```powershell
pip install <package>
pip freeze > requirements.txt
```

3. Pour recréer l’environnement sur une autre machine :  

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

4. Ignorer certains fichiers dans Git : `.gitignore` recommandé pour :  

```text
venv/
__pycache__/
node_modules/
*.pyc
```

## ✅ État d’avancement du projet

Ce projet est en cours de développement pour répondre au cahier des charges du projet **TISSÉA**.  
Ci-dessous un résumé des tâches déjà effectuées et de celles encore à réaliser.

---

#!/bin/bash

cat << 'EOF' > README.md
# 📘 README – Projet API Tissea

## ✅ Ce qui est fait

### 1️⃣ Structure générale
- FastAPI opérationnel (`main.py`, `database.py`, arborescence `models/` et `schemas/`)  
- Connexion à MariaDB via SQLModel et `engine`  
- Création automatique des tables au démarrage avec `SQLModel.metadata.create_all(engine)`  

### 2️⃣ Utilisateurs (Users)
- **POST /users** → création utilisateur avec hash SHA256 du mot de passe  
- **GET /users/{id}** → lecture utilisateur par ID  
- **PUT /update/users/{id}** → mise à jour des champs utilisateur (username, email, password)  
- **DELETE /delete/users/{id}** → suppression utilisateur  
- **GET /allusers** → liste de tous les utilisateurs  
- Gestion des doublons email/username lors de la création et mise à jour  

### 3️⃣ Catégories (Category)
- **POST /api/creat/category** → création catégorie  
- **GET /api/category/{id}** → lecture catégorie par ID  
- **PUT /api/update/category/{id}** → mise à jour catégorie  
- **DELETE /api/delete/category/{id}** → suppression catégorie  
- **GET /api/allcategory** → liste de toutes les catégories  

### 4️⃣ Lignes de transport (TransportLine)
- **POST /api/creat/line** → création ligne de transport (avec vérification de la catégorie)  
- **GET /api/line/{id}** → lecture ligne par ID  
- **PUT /api/update/line/{id}** → mise à jour ligne de transport  
- **DELETE /api/delete/line/{id}** → suppression ligne (simple, ne supprime pas les arrêts liés)  
- **GET /api/allline** → liste de toutes les lignes  

### 5️⃣ Arrêts (Stop)
- **POST /api/creat/stop** → création arrêt (vérification que la ligne existe)  
- **GET /api/stop/{id}** → lecture arrêt par ID  
- **PUT /api/update/stop/{id}** → mise à jour arrêt  
- **DELETE /api/delete/stop/{id}** → suppression arrêt  
- **GET /api/allstop** → liste de tous les arrêts  

---

## 🚧 Ce qui reste à faire / améliorations possibles

### 🔐 Authentification & sécurité
- Ajouter la connexion utilisateur `/api/users/login`  
- Implémenter JWT pour sécuriser les routes  
- Restreindre l’accès à tous les endpoints (sauf signup/login)  

### 🗺️ Gestion du réseau de transport
- Endpoints avancés pour liaisons catégories/lignes/arrêts :  
  - `GET /api/categories/{id}/lines` → lister toutes les lignes d’une catégorie  
  - `GET /api/lines/{id}/stops` → lister tous les arrêts d’une ligne  
  - `POST /api/lines/{id}/stops` → ajouter un arrêt sur une ligne  
  - `DELETE /api/lines/{line_id}/stops/{stop_id}` → suppression d’un arrêt d’une ligne (pour l’instant, tu as juste `/api/delete/stop/{id}` qui supprime l’arrêt directement)  

### 📏 Statistiques et calculs (GPS)
- Calcul de distances entre arrêts ou lignes avec **geopy**  

### 🖥️ Mini-Frontend
- Carte Leaflet pour afficher les lignes et arrêts  
- Pages Inscription / Connexion  
- Appels API sécurisés avec token JWT  

### 🧪 Tests & Documentation
- Tests unitaires pour toutes les routes  
- Documentation OpenAPI + résumé manuel  
- Diagramme base de données et structure des endpoints  

---

## 🧭 Notes techniques / choix faits
- DELETE ligne ne supprime pas automatiquement les arrêts liés → choix simplifié pour ne pas gérer les cascades complexes.  
- Hashage SHA256 utilisé pour l’instant → à remplacer par bcrypt pour la production.  
- Les champs supplémentaires dans les schemas (`mots`, `motsWTF`) servent uniquement à tester l’affichage sans exposer le mot de passe.  

EOF

echo "README.md créé avec succès !"

