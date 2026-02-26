## E‑commerce (Django + React + Postgres + Redis + Stripe)

**Projet : لمسة هاجر** — Site déployé : [Vercel](https://creation-projet.vercel.app) | Backend : [Render](https://creation-projet.onrender.com)

📄 **Documentation technique (rapport + référence)** : [DOCUMENTATION-TECHNIQUE.md](./DOCUMENTATION-TECHNIQUE.md) — à ouvrir sur GitHub pour la lire en entier.

---

### Pré‑requis

- Docker + Docker Compose
- Python 3
- Node.js + npm

### Démarrer Postgres + Redis

```bash
cp .env.example .env
docker compose up -d
```

### Backend (Django)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_products
python manage.py runserver
```

Admin: `http://localhost:8000/admin/`

### Frontend (React)

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

App: `http://localhost:5173/`

### Paiement Stripe (dev)

- Mettre `STRIPE_SECRET_KEY` dans `.env`
- Exposer le webhook Stripe vers `http://localhost:8000/api/payments/webhook/stripe/`
- Le bouton “Payer avec Stripe” appelle `POST /api/payments/create-checkout-session/` et redirige vers Stripe Checkout.

