# Documentation technique — لمسة هاجر

Site e-commerce (boutique en ligne) : frontend React déployé sur Vercel, backend Django et base PostgreSQL sur Render, paiement Stripe.

---

# Partie I — Rapport du projet

## 1. Introduction

Ce projet est une boutique en ligne nommée **لمسة هاجر**, qui signifie « La touche de Hajar ». Cette documentation technique décrit la stack (Django, React, PostgreSQL, Stripe), l’architecture, l’installation en local, le système de versioning et le déploiement du site.

L’objectif était de créer une application web e-commerce avec les fonctionnalités suivantes : création de compte et connexion, catalogue de produits à vendre, et système de paiement pour un achat immédiat. Au niveau technique : base de données PostgreSQL, Redis pour le cache, paiement avec Stripe, code versionné (Git). Pour l’interface : React (JavaScript), et Python / Django pour le backend. Cette stack a été validée et le projet a été poursuivi dans ce sens.

---

## 2. Vision du projet

L’objectif était de créer une plateforme e-commerce moderne et sécurisée (« achat immédiat ») permettant de gérer un catalogue de produits, des comptes utilisateurs et des transactions réelles. Le site devait respecter les points suivants :

- **Authentification :** création de compte et connexion sécurisée. Les utilisateurs doivent pouvoir créer un compte et se connecter par la suite.
- **Catalogue :** gestion dynamique des produits et catégories via PostgreSQL. Des produits devaient être présents sur le site afin que les utilisateurs puissent les acheter immédiatement.
- **Paiement :** intégration de Stripe pour sécuriser les transactions.
- **Performance :** utilisation de Redis pour le cache et les sessions (en local ; optionnel en production selon l’hébergement).

---

## 3. Architecture technique (validée et déployée)

Nous avons séparé le « cerveau » (backend) de la « partie visible » (frontend) pour plus de flexibilité.

**Stack technologique :**

- **Frontend :** React avec JavaScript, hébergé sur **Vercel**.
- **Backend :** Python / Django REST Framework, hébergé sur **Render**.
- **Base de données :** **PostgreSQL**, pour la gestion des transactions et la cohérence des données. PostgreSQL garantit que les opérations sont traitées de manière fiable ; en cas de panne, les données restent cohérentes. Il stocke les utilisateurs, les produits et les commandes.
- **Versioning :** Git / GitHub — le code source est entièrement versionné.

---

## 4. Structure du système (apps Django)

Le backend a été découpé en modules logiques :

- **accounts :** gestion du modèle User (inscription, connexion).
- **catalog :** modèles Category et Product (avec le champ `image_url` pour les visuels des produits).
- **cart :** gestion du panier (lignes, quantités) avant passage en commande.
- **orders :** gestion des commandes et des statuts (Pending, Paid, etc.), pour avoir une vision claire sur les commandes passées.
- **payments :** tunnel de paiement et webhooks Stripe pour confirmer les achats de manière sécurisée.

---

## 5. Réalisations en production (défis relevés)

Pour passer de « ça marche en local » à « c’est en ligne pour tout le monde », les points suivants ont été mis en place :

- **Gestion des webhooks :** configuration d’un endpoint secret (`/api/payments/webhook/stripe/`) pour que Stripe notifie le serveur Render du succès du paiement.
- **Sécurité CORS :** autorisation stricte pour que le domaine Vercel puisse communiquer avec l’API Render.
- **Fichiers statiques (WhiteNoise) :** configuration pour que l’interface d’administration Django soit disponible avec son design en production.
- **Base de données cloud :** migration des données locales vers PostgreSQL sur Render.

---

## 6. Guide de gestion (Admin)

L’interface d’administration permet une gestion complète sans toucher au code :

- **URL :** https://creation-projet.onrender.com/admin/
- **Suivi des ventes :** visualisation des commandes avec le statut « Paid ».
- **Gestion du catalogue :** ajout / suppression de catégories et de produits (ex. suppression de la catégorie « Accessoires »).

---

## 7. Conclusion technique

Le projet respecte les standards actuels du web : séparation des préoccupations (React / Django), traitement asynchrone des paiements via webhooks, et déploiement continu — chaque modification poussée sur GitHub est automatiquement reflétée sur Vercel et Render.

---

# Partie II — Référence technique

## 1. Vue d’ensemble

- **Nom du site :** لمسة هاجر (Lamsat Hajar)
- **Type :** E-commerce (catalogue, panier, commandes, paiement Stripe)
- **Frontend :** React 19 + Vite 7, hébergé sur **Vercel**
- **Backend :** Django 6 + Django REST Framework, hébergé sur **Render**
- **Base de données :** PostgreSQL (Render)
- **Cache / session :** Redis (optionnel en local avec Docker)
- **Paiement :** Stripe (Checkout Session + webhook)

---

## 2. Stack technique

| Couche        | Technologie |
|---------------|-------------|
| Frontend      | React 19, React Router 7, Vite 7 |
| Backend       | Django 6, djangorestframework, djangorestframework-simplejwt |
| Base de données | PostgreSQL (psycopg) |
| Auth API      | JWT (access + refresh token) |
| Paiement      | Stripe (API + webhook) |
| CORS / statiques | django-cors-headers, whitenoise |
| Déploiement   | Vercel (frontend), Render (backend + DB) |

---

## 3. Architecture

```
[Utilisateur]
      │
      ▼
[Vercel]  ←  Frontend React (SPA)
      │         • Pages : Accueil, Catégories, Produit, Panier, Commandes, Login, Register
      │         • Appels API vers le backend
      │
      ▼
[Render]  ←  Backend Django (API REST)
      │         • /api/auth/     (inscription, connexion, JWT)
      │         • /api/         (catalogue, catégories, produits)
      │         • /api/cart/    (panier)
      │         • /api/orders/  (commandes)
      │         • /api/payments/ (Stripe checkout + webhook)
      │
      ├──► [PostgreSQL]  (données : users, catégories, produits, panier, commandes)
      └──► [Stripe]      (paiement et webhook)
```

---

## 4. Structure du projet

```
Projet app web/
├── backend/                    # Django
│   ├── config/                  # Settings, urls principaux
│   ├── accounts/                # Auth (register, login, JWT)
│   ├── catalog/                 # Catégories, produits, seed
│   ├── cart/                    # Panier
│   ├── orders/                  # Commandes
│   ├── payments/                # Stripe (checkout, webhook)
│   ├── manage.py
│   └── requirements.txt
├── frontend/                    # React + Vite
│   ├── public/                  # Assets statiques (ex. /images/)
│   ├── src/
│   │   ├── api/                 # Client API (fetch, base URL)
│   │   ├── auth.js              # Stockage JWT, refresh
│   │   ├── App.jsx, App.css
│   │   └── pages/               # HomePage, CategoryPage, ProductDetailPage, CartPage, etc.
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .env                         # Variables locales (non versionné)
├── ENV-PRODUCTION.md            # Rappel des variables Vercel / Render
├── README.md                    # Démarrage rapide
└── DOCUMENTATION-TECHNIQUE.md   # Ce fichier
```

---

## 5. Installation et développement local (étape par étape)

### 5.1 Prérequis

- **Python 3** (recommandé 3.11+)
- **Node.js** et **npm**
- **Docker** et **Docker Compose** (pour PostgreSQL et Redis en local)
- Un compte **Stripe** (mode test pour le dev)

### 5.2 Variables d’environnement locales

À la racine du projet, créer un fichier `.env` (à partir de `.env.example` s’il existe) avec au minimum :

```env
# Django
DJANGO_DEBUG=1
DJANGO_SECRET_KEY=dev-secret-key-change-me
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL (local ou Docker)
POSTGRES_DB=ecommerce
POSTGRES_USER=ecommerce
POSTGRES_PASSWORD=ecommerce
POSTGRES_HOST=localhost
POSTGRES_PORT=5433

# Redis (optionnel, pour cache/session)
REDIS_URL=redis://localhost:6379/1

# Stripe (clés test)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Frontend (pour le dev)
FRONTEND_URL=http://localhost:5173
VITE_API_BASE_URL=http://localhost:8000
```

Le frontend lit `VITE_API_BASE_URL` au build ; en local avec `npm run dev`, il utilise souvent un proxy ou la variable définie dans `frontend/.env`.

### 5.3 Lancer PostgreSQL (et optionnellement Redis)

Si tu utilises Docker pour la base locale :

```bash
# À la racine du projet
docker compose up -d
```

Vérifier que `POSTGRES_HOST=localhost` et `POSTGRES_PORT=5433` (ou le port exposé par Docker) correspondent à ton `.env`.

### 5.4 Backend Django

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_categories
python manage.py seed_products
python manage.py runserver
```

- **Admin Django :** http://localhost:8000/admin/
- **API :** http://localhost:8000/api/

### 5.5 Frontend React

Dans un autre terminal :

```bash
cd frontend
npm install
# Si besoin : créer frontend/.env avec VITE_API_BASE_URL=http://localhost:8000
npm run dev
```

- **Application :** http://localhost:5173/

### 5.6 Paiement Stripe en local

- Dans le tableau de bord Stripe (mode test), créer un **webhook** pointant vers :  
  `http://localhost:8000/api/payments/webhook/stripe/`  
  (pour exposer le backend en local, utiliser par exemple **ngrok** ou l’outil Stripe CLI).
- Mettre `STRIPE_WEBHOOK_SECRET` dans le `.env` après création du webhook.

---

## 6. API — principaux endpoints

| Méthode | URL | Description |
|--------|-----|-------------|
| GET | `/api/categories/` | Liste des catégories (racines) |
| GET | `/api/categories/<slug>/` | Détail catégorie + sous-catégories / produits |
| GET | `/api/products/<id>/` | Détail d’un produit |
| POST | `/api/auth/register/` | Inscription |
| POST | `/api/auth/login/` | Connexion (retourne access + refresh JWT) |
| POST | `/api/auth/token/refresh/` | Rafraîchir l’access token |
| GET | `/api/cart/` | Contenu du panier (authentifié) |
| POST | `/api/cart/` | Ajouter une ligne au panier |
| PATCH | `/api/cart/<id>/` | Modifier quantité |
| DELETE | `/api/cart/<id>/` | Supprimer une ligne |
| GET | `/api/orders/` | Liste des commandes de l’utilisateur |
| POST | `/api/payments/create-checkout-session/` | Créer une session Stripe Checkout |
| POST | `/api/payments/webhook/stripe/` | Webhook Stripe (événements paiement) |

L’authentification se fait via le header :  
`Authorization: Bearer <access_token>`.

---

## 7. Déploiement production

### 7.1 Frontend (Vercel)

- Projet connecté au dépôt Git (ex. `main`).
- **Variable d’environnement :**  
  `VITE_API_BASE_URL` = `https://creation-projet.onrender.com` (ou l’URL de ton backend Render).
- Chaque push sur la branche déployée déclenche un nouveau build et déploiement.

### 7.2 Backend + base (Render)

- **Service Web :** backend Django (build : `pip install -r requirements.txt`, start : `gunicorn`).
- **Base PostgreSQL :** créée sur Render (Internal ou External selon l’offre).
- **Variables d’environnement Render** (à renseigner dans le dashboard) :
  - `POSTGRES_*` (host, user, password, db, port) fournis par Render pour la base.
  - `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` (ex. `creation-projet.onrender.com`).
  - `CORS_ALLOWED_ORIGINS` = URL du frontend (ex. `https://creation-projet.vercel.app`).
  - `FRONTEND_URL` = même URL frontend (pour redirections après paiement).
  - `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` (compte Stripe production ou test).
- **Webhook Stripe en prod :** URL = `https://creation-projet.onrender.com/api/payments/webhook/stripe/`.

Le détail des variables est rappelé dans **ENV-PRODUCTION.md**.

---

## 8. Commandes utiles

| Commande | Où | Description |
|----------|-----|-------------|
| `python manage.py migrate` | backend | Appliquer les migrations |
| `python manage.py createsuperuser` | backend | Créer un compte admin |
| `python manage.py seed_categories` | backend | Créer les catégories (Femme, sous-catégories) |
| `python manage.py seed_products` | backend | Créer les produits (robe, abaya, parfums, sacs) |
| `python manage.py remove_accessoires` | backend | Supprimer la catégorie Accessoires (si présente) |
| `npm run build` | frontend | Build de production (sortie dans `dist/`) |
| `npm run dev` | frontend | Serveur de dev Vite |

---

## 9. Contenu et médias

- **Images produits :** stockées dans `frontend/public/images/` (servies en statique sous `/images/...`). Les produits en base ont un champ `image_url` (ex. `/images/robe-simple-bleu-marine.png`).
- **Modifier un produit :** soit via l’admin Django (Render en prod), soit en modifiant le seed puis en re-seedant (en local ou en pointant la commande vers la base Render avec les variables d’environnement adéquates).

---

## 10. Résumé pour un nouveau développeur

1. Cloner le dépôt, créer `.env` à la racine (voir section 5.2).
2. Lancer PostgreSQL (Docker ou autre), puis `backend` : venv, `pip install`, `migrate`, `createsuperuser`, `seed_categories`, `seed_products`, `runserver`.
3. Lancer le frontend : `npm install`, `npm run dev`.
4. Pour les paiements en local : configurer Stripe (clés test + webhook vers le backend exposé).
5. En production : configurer Vercel (frontend) et Render (backend + PostgreSQL) comme indiqué en section 7 et dans ENV-PRODUCTION.md.

---

*Documentation générée pour le projet لمسة هاجر. Dernière mise à jour : février 2026.*
