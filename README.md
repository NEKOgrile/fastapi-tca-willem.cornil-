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

### 🧩 Fonctionnalités terminées

- ✅ **Structure FastAPI** opérationnelle (`main.py`, `database.py`, arborescence models/schemas/routers)
- ✅ **Connexion à MariaDB** via SQLModel et identifiant.json
- ✅ **CRUD complet pour les utilisateurs**
- ✅ **Hashage SHA256** des mots de passe (à remplacer par bcrypt pour la version finale)
- ✅ **Création automatique des tables au démarrage**
- ✅ **Test API fonctionnel** via `/docs`
- ✅ **Base de données complète importée** (categories, transport_lines, stops, users)

---

### 🚧 Fonctionnalités à implémenter

#### 🔐 Authentification & Sécurité (Priorité haute)
- [ ] Ajouter la **connexion utilisateur** (`/api/users/login`)
- [ ] Implémenter **JWT** (connexion, vérification, dépendance `get_current_user`)
- [ ] Restreindre l’accès à tous les endpoints de l’API (sauf signup/login)

#### 🗺️ Gestion du réseau de transport (Priorité haute)
- ✅ Créer les **modèles SQLModel** : `Category`, `TransportLine`, `Stop`
- ✅ Créer les **schemas Pydantic** correspondants dans `schemas/`
- [ ] Implémenter les routes suivantes :
  - [ ] `GET /api/categories/{id}/lines` → liste des lignes d’une catégorie  
  - [ ] `GET /api/lines/{id}` → détails d’une ligne (heures, arrêts, etc.)  
  - [ ] `GET /api/lines/{id}/stops` → liste détaillée des arrêts  
  - [ ] `POST /api/lines/{id}/stops` → ajout d’un arrêt  
  - [ ] `PUT /api/lines/{id}` → mise à jour d’une ligne  
  - [ ] `DELETE /api/lines/{line_id}/stops/{stop_id}` → suppression d’un arrêt  

#### 📏 Statistiques et calculs (Priorité moyenne)
- [ ] `GET /api/stats/distance/stops/{id1}/{id2}` → calcul de la distance entre deux arrêts  
- [ ] `GET /api/stats/distance/lines/{id}` → calcul de la distance totale d’une ligne  
- [ ] Utiliser la librairie **geopy** (`geodesic`) pour les distances GPS  

#### 🖥️ Mini-Frontend (Priorité moyenne)
- [ ] Page **Accueil**
- [ ] Page **Inscription / Connexion**
- [ ] Page **Carte Leaflet** affichant au moins une ligne (ex. Métro B)
- [ ] Appels API sécurisés avec token JWT

#### 🧪 Tests & Documentation (Priorité basse)
- [ ] Tests unitaires (`pytest` ou `Vitest` selon choix)
- [ ] Dossier `docs/` avec :
  - Schéma de la base de données
  - Documentation API (OpenAPI + résumé manuel)
- [ ] Préparer le **diaporama de soutenance**

---

### 🧭 Ordre recommandé de développement

1️⃣ → **Ajouter JWT & route de connexion**  
2️⃣ → **Créer les modèles Category / Line / Stop**  
3️⃣ → **Implémenter les endpoints REST principaux**  
4️⃣ → **Tester les routes `/stats/distance/...`**  
5️⃣ → **Protéger tous les endpoints par JWT**  
6️⃣ → **Créer le mini-frontend Leaflet**  
7️⃣ → **Finaliser la documentation et la soutenance**

---

### 🗓️ Prochain objectif

> 🎯 **Prochaine étape : Authentification JWT complète**
>
> - Création du module `auth.py`
> - Ajout de `/api/users/login`
> - Génération et validation des tokens
> - Protection des routes avec `Depends(get_current_user)`

