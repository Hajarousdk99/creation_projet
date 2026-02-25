# Rapport d’analyse – Projet Boutique Djellaba

Analyse du code (backend Django, frontend React, déploiement, sécurité, fonctionnalités) et points à améliorer.

---

## 1. Ce qui est en place et fonctionne

- **Backend Django** : auth JWT (login, register, token refresh), catalog (catégories, produits), panier (CRUD), paiement Stripe (création session, confirmation, webhook), commandes (modèles + admin).
- **Frontend React** : accueil, catégories, détail produit, panier, connexion/inscription, checkout succès/annulation, appel API avec gestion d’erreur (message adapté prod/local).
- **Déploiement** : backend Render (PostgreSQL, gunicorn), frontend Vercel, `STATIC_ROOT` pour collectstatic, `ENV-PRODUCTION.md` pour les variables.
- **Sécurité de base** : CORS configurable, `AUTH_USER_MODEL` personnalisé, validation mot de passe Django, webhook Stripe vérifié par signature.
- **Données** : seed catégories/produits, envoi d’email de confirmation après paiement (backend console en dev).

---

## 2. Manques et recommandations

### 2.1 API « Mes commandes »

- **Constat** : Le modèle `Order` existe et est utilisé (création au checkout, passage en « paid »), mais il n’y a **aucune route API** pour qu’un utilisateur connecté liste ses commandes.
- **Impact** : L’utilisateur ne peut pas voir l’historique de ses commandes dans l’app.
- **Recommandation** : Ajouter une app ou des vues sous `orders` (ex. `GET /api/orders/`) avec `permission_classes = [IsAuthenticated]`, sérializer les commandes (avec items), et inclure les URLs dans `config/urls.py`. Côté frontend, ajouter une page « Mes commandes » et un lien dans la nav.

---

### 2.2 Tests

- **Constat** : Les fichiers `catalog/tests.py`, `accounts/tests.py`, `payments/tests.py`, `orders/tests.py`, `cart/tests.py` sont vides (uniquement le squelette `TestCase`).
- **Impact** : Aucune garantie automatique lors de changements (régression auth, panier, paiement, catalog).
- **Recommandation** : Écrire au minimum des tests pour : login/register, liste catégories/produits, panier (ajout/modification/suppression), création de session Stripe (mock), confirmation de commande (session_id). Utiliser `pytest-django` ou les `TestCase` Django + `APIClient`.

---

### 2.3 Sécurité production (Django)

- **Constat** : Aucun réglage explicite pour HTTPS / en-têtes de sécurité (pas de `SECURE_SSL_REDIRECT`, `SECURE_HSTS_*`, `X_FRAME_OPTIONS`, etc. dans `settings.py`).
- **Impact** : En production derrière un reverse proxy (ex. Render), les redirects HTTPS et HSTS sont souvent gérés par la plateforme, mais une config explicite rend le comportement clair et renforce la sécurité.
- **Recommandation** : Dans `settings.py`, ajouter un bloc conditionnel `if not DEBUG:` avec par exemple :
  - `SECURE_SSL_REDIRECT = True`
  - `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")` (si Render envoie ce header)
  - `SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True`
  - `SECURE_HSTS_SECONDS = 31536000`, `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`, `SECURE_HSTS_PRELOAD = True`
  - Vérifier la doc Render pour le proxy et adapter si besoin.

---

### 2.4 Secret key et DEBUG en production

- **Constat** : `SECRET_KEY` et `DEBUG` sont lus depuis l’environnement (`.env` / variables Render), ce qui est bon. En production il faut s’assurer que `DEBUG=False` et que `SECRET_KEY` est une valeur forte et unique.
- **Recommandation** : Dans `ENV-PRODUCTION.md` (ou la doc déploiement), rappeler explicitement : **ne jamais** laisser `DEBUG=True` ni une `SECRET_KEY` faible en production. Sur Render, vérifier que les variables sont bien définies.

---

### 2.5 Rafraîchissement du token JWT (frontend)

- **Constat** : Le frontend stocke `access` et `refresh` dans `localStorage` et envoie le token dans `Authorization`, mais il n’y a **pas de logique** pour rafraîchir le token quand l’API renvoie 401 (token expiré).
- **Impact** : Après 30 minutes (durée de vie du access token), l’utilisateur est de fait déconnecté sans message clair ni tentative de refresh.
- **Recommandation** : Dans `api/client.js` (ou un intercepteur), en cas de réponse 401, appeler `POST /api/auth/token/refresh/` avec le refresh token, mettre à jour le token, puis réessayer la requête. Si le refresh échoue, rediriger vers la page de connexion et supprimer les tokens.

---

### 2.6 Page 404 (frontend)

- **Constat** : Aucune `Route` avec `path="*"` (ou équivalent) pour les URLs inconnues.
- **Impact** : Une URL inexistante (ex. `/page-inexistante`) peut afficher une page vide ou un comportement peu clair.
- **Recommandation** : Ajouter une route catch-all qui affiche une page « Page non trouvée » et un lien vers l’accueil.

---

### 2.7 Email en production

- **Constat** : `EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"` est en dur dans `settings.py`. Les emails de confirmation de commande sont donc uniquement affichés dans la console (ou les logs) en production.
- **Impact** : L’utilisateur ne reçoit pas d’email de confirmation en production.
- **Recommandation** : Lire le backend email depuis l’environnement (ex. `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`). En prod, configurer un service (SendGrid, Mailgun, SMTP Render, etc.) et définir les variables dans Render. Garder le backend console en dev si `DEBUG=True` ou si une variable `EMAIL_BACKEND` n’est pas définie.

---

### 2.8 Documentation déploiement

- **Constat** : `README.md` décrit surtout le lancement en local (Docker, backend, frontend). `ENV-PRODUCTION.md` liste les variables Vercel/Render.
- **Recommandation** : Compléter le README (ou un `DEPLOIEMENT.md`) avec : URL du site (ex. creation-projet.vercel.app), URL du backend (creation-projet.onrender.com), étapes Render (Build/Start, env), étapes Vercel (root `frontend`, `VITE_API_BASE_URL`), configuration du webhook Stripe (URL complète : `https://creation-projet.onrender.com/api/payments/webhook/stripe/`), et rappel de lancer seed + createsuperuser (ex. en local vers la base Render).

---

### 2.9 Gestion du stock (optionnel)

- **Constat** : Le modèle `Product` a un champ `stock` mais aucun code ne le décrémente à la validation du panier / paiement.
- **Impact** : Risque de vendre plus que le stock disponible.
- **Recommandation** : Lors du passage de la commande en « paid » (dans `_mark_order_paid_and_after` ou équivalent), décrémenter le `stock` des produits concernés (avec `select_for_update()` et transaction pour éviter les race conditions). Optionnellement, refuser l’ajout au panier ou le checkout si la quantité demandée dépasse le stock.

---

## 3. Synthèse priorisée

| Priorité | Sujet | Action courte |
|----------|--------|----------------|
| Haute    | API « Mes commandes » | Ajouter `GET /api/orders/` + page front « Mes commandes ». |
| Haute    | Refresh token JWT | Gérer 401 + appel token refresh + retry dans le client API. |
| Moyenne  | Tests | Ajouter tests auth, catalog, panier, paiement (Stripe mocké). |
| Moyenne  | Sécurité HTTPS/HSTS | Activer `SECURE_*` et cookies sécurisés quand `DEBUG=False`. |
| Moyenne  | Email en prod | Configurer un vrai backend email via variables d’env. |
| Basse    | Page 404 | Route catch-all + composant « Page non trouvée ». |
| Basse    | Stock | Décrémenter le stock à la confirmation de paiement. |
| Doc      | Déploiement | Compléter README / DEPLOIEMENT avec URLs et webhook Stripe. |

---

## 4. Fichiers modifiés / à créer (pour les correctifs)

- **Backend** : `config/settings.py` (sécurité prod, email), `config/urls.py` (inclure `orders.urls` si créé), `orders/views.py` + `orders/serializers.py` + `orders/urls.py` (API commandes).
- **Frontend** : `src/api/client.js` (refresh token sur 401), `src/App.jsx` (route 404), nouvelle page `MesCommandesPage.jsx` + route et lien nav.
- **Doc** : `README.md` ou `DEPLOIEMENT.md` (URLs, webhook, variables).

Ce rapport peut servir de base pour planifier les prochaines tâches (sprints ou tickets).
