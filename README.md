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

#########################################
# 🚀 PROJET FASTAPI - TISSÉA - TODO LIST
#########################################

# ===============================
# ✅ ÉTAPES DÉJÀ RÉALISÉES
# ===============================

[✅] Structure FastAPI de base fonctionnelle
[✅] Connexion à MariaDB (SQLModel + identifiant.json)
[✅] Table "users" (CRUD complet)
[✅] Hashage des mots de passe (sha256 temporaire)
[✅] Fichier README clair et structuré
[✅] Base de données MariaDB opérationnelle :
      - categories(id, name)
      - transport_lines(id, name, category_id, start_time, end_time)
      - stops(id, name, latitude, longitude, stop_order, line_id)
      - users(id, username, email, hashed_password, created_at)

# ===============================
# 🔥 ÉTAPES PRIORITAIRES À FAIRE
# ===============================

[⬜] Ajouter l’authentification JWT :
       -> Route POST /api/users/login
       -> Token JWT + dépendance get_current_user
       -> Sécuriser toutes les routes API

[⬜] Créer les modèles dans models.py :
       -> Category (avec ou sans relation lines)
       -> TransportLine (avec relation category et stops)
       -> Stop (avec relation line)

[⬜] Créer les schémas correspondants dans schemas.py

[⬜] Implémenter les routes principales :
       -> GET /api/categories/{id}/lines
       -> GET /api/lines/{id}
       -> GET /api/lines/{id}/stops
       -> POST /api/lines/{id}/stops
       -> PUT /api/lines/{id}
       -> DELETE /api/lines/{line_id}/stops/{stop_id}

[⬜] Ajouter les endpoints de calculs de distance :
       -> GET /api/stats/distance/stops/{id1}/{id2}
       -> GET /api/stats/distance/lines/{id}
       -> Utiliser geopy.distance.geodesic()

[⬜] Protéger tous les endpoints (sauf signup/login) avec JWT

[⬜] Vérifier cohérence entre la BDD MariaDB et les modèles FastAPI

# ===============================
# 💪 ÉTAPES BONUS / OPTIONNELLES
# ===============================

[⬜] Remplacer hashlib par bcrypt pour sécuriser les mots de passe
[⬜] Ajouter des tests unitaires avec pytest
[⬜] Créer un mini frontend (HTML + JS + Leaflet)
       -> Pages : accueil, inscription, connexion
       -> Carte affichant les lignes de transport
[⬜] Ajouter un dossier "docs/" :
       -> Schéma de la base (diagramme)
       -> Documentation API
[⬜] Générer un diaporama de soutenance :
       -> Présentation du projet
       -> Modèle de données
       -> Démo API + Frontend
       -> Améliorations possibles

# ===============================
# 🧭 PRIORITÉ DE DÉVELOPPEMENT
# ===============================

1️⃣ - Authentification JWT (Login + Sécurité)
2️⃣ - Modèles + Schémas (Category, Line, Stop)
3️⃣ - Endpoints REST principaux
4️⃣ - Calculs de distance avec Geopy
5️⃣ - Protection JWT sur les routes
6️⃣ - Mini Frontend Leaflet
7️⃣ - Tests + Documentation + Soutenance

#########################################
# 🔚 FIN DU SUIVI DE PROJET TISSÉA
#########################################

