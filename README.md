
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

# Lancer le serveur FastAPI
uvicorn main:app --reload
```

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

1. Mettre à jour `DATABASE_URL` dans `database.py` avec vos identifiants MariaDB.
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

