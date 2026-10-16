# Real-Time E-commerce Marketplace with Recommendation Engine

Professional Django implementation package based on the supplied project blueprint.

## Implemented in this MVP

- Custom user roles
- Product categories and catalog
- Search/filter/order API
- Seller ownership checks
- Inventory model and stock ledger
- Transactional stock reservation with `select_for_update()`
- Persistent cart
- Idempotent checkout key
- Order snapshots
- Demo payment confirmation
- DRF APIs
- Swagger/OpenAPI docs
- Simple popularity/content-based recommendation service
- PostgreSQL
- Redis/Celery configuration
- Docker Compose
- Demo data command
- Health endpoints
- Django Admin
- Basic automated checkout test

## Architecture

```text
Browser / API Client
        |
        v
Django + Django REST Framework
        |
  +-----+-------------+----------------+
  |                   |                |
PostgreSQL           Redis          Celery Worker
  |
  +--> Catalog / Inventory / Cart / Orders
  +--> Recommendation interaction data
```

## Important

This repository is a strong portfolio/interview implementation base, not a claim that every feature in the original specification has already been built. See `RUNNING_STEPS.md` for exact setup and execution instructions.

## Run

Recommended:

```bash
cp .env.example .env
docker compose up -d --build
docker compose exec web python manage.py makemigrations accounts catalog inventory cart orders recommendations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py seed_demo_data
```

Open:

- Storefront: http://localhost:8000/
- Swagger: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/
# Real-time-e-commerce-marketplace-with-recommendation-engine
