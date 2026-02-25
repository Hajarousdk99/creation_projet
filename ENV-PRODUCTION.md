# Variables à configurer en production (le .env local n’est pas utilisé)

## Sur Vercel (projet creation-projet)

**Settings** → **Environment Variables** (du projet, pas du Team) :

| Variable             | Valeur                              | Environnement |
|----------------------|-------------------------------------|---------------|
| VITE_API_BASE_URL    | https://creation-projet.onrender.com | Production    |

Puis **Deployments** → **Redeploy** pour que le build prenne la variable.

---

## Sur Render (service creation_projet)

**Environment** :

| Variable               | Valeur (exemple) |
|------------------------|------------------|
| POSTGRES_HOST          | dpg-xxx-a.frankfurt-postgres.render.com (External Database URL de ta base) |
| POSTGRES_USER         | (celui de ta base) |
| POSTGRES_PASSWORD     | (celui de ta base) |
| POSTGRES_DB           | (celui de ta base) |
| POSTGRES_PORT         | 5432 |
| DJANGO_ALLOWED_HOSTS  | creation-projet.onrender.com |
| CORS_ALLOWED_ORIGINS  | https://creation-projet.vercel.app |
| FRONTEND_URL          | https://creation-projet.vercel.app |
| (+ DJANGO_SECRET_KEY, STRIPE_*, etc.) | |

Puis **Save** et **Manual Deploy**.

---

Ton fichier `.env` en local reste avec `localhost` pour développer ; il n’est pas envoyé sur Git et n’a aucun effet sur le site en ligne.
