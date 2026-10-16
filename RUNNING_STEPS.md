# How to Run the Project

This code package implements a professional MVP based on the supplied marketplace blueprint.

## Option A — Docker (recommended)

### 1. Install prerequisites

Install:

- Docker Desktop
- Git (optional, if you want source control)

### 2. Open the project folder

```bash
cd ecommerce_marketplace_django
```

### 3. Create local environment file

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Windows CMD:

```cmd
copy .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

### 4. Build containers

```bash
docker compose build
```

### 5. Start PostgreSQL, Redis, Django and Celery

```bash
docker compose up -d
```

### 6. Create migrations

```bash
docker compose exec web python manage.py makemigrations accounts catalog inventory cart orders recommendations
```

### 7. Apply migrations

```bash
docker compose exec web python manage.py migrate
```

### 8. Create admin user

```bash
docker compose exec web python manage.py createsuperuser
```

### 9. Create demo products

```bash
docker compose exec web python manage.py seed_demo_data
```

### 10. Open the application

Storefront:

```text
http://localhost:8000/
```

Django Admin:

```text
http://localhost:8000/admin/
```

Swagger API documentation:

```text
http://localhost:8000/api/docs/
```

Readiness health check:

```text
http://localhost:8000/health/ready/
```

### 11. Run tests

```bash
docker compose exec web python manage.py test
```

### 12. View logs

```bash
docker compose logs -f web
```

Celery worker:

```bash
docker compose logs -f worker
```

### 13. Stop the project

```bash
docker compose down
```

To also delete the local database volume:

```bash
docker compose down -v
```

---

# Option B — Run locally without Docker

## 1. Install

- Python 3.12
- PostgreSQL 16
- Redis 7

## 2. Create virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Create PostgreSQL database

Example:

```sql
CREATE USER marketplace_user WITH PASSWORD 'marketplace_password';
CREATE DATABASE marketplace_db OWNER marketplace_user;
```

## 5. Create `.env`

Copy `.env.example` and change the database hostname from `db` to `localhost`:

```dotenv
DATABASE_URL=postgresql://marketplace_user:marketplace_password@localhost:5432/marketplace_db
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
```

## 6. Migrate

```bash
python manage.py makemigrations accounts catalog inventory cart orders recommendations
python manage.py migrate
```

## 7. Create admin

```bash
python manage.py createsuperuser
```

## 8. Seed data

```bash
python manage.py seed_demo_data
```

## 9. Run Django

```bash
python manage.py runserver
```

## 10. Run Celery in another terminal

```bash
celery -A config worker -l info
```

---

# API Demo Flow

## Register buyer

```http
POST /api/v1/accounts/register/
Content-Type: application/json

{
  "username": "buyer1",
  "email": "buyer1@example.com",
  "password": "Buyer123!"
}
```

## Browse products

```http
GET /api/v1/catalog/products/?q=watch&ordering=price
```

## Add cart item

Login through Django session first, then:

```http
POST /api/v1/cart/items/

{
  "product": 1,
  "quantity": 1
}
```

## Checkout

```http
POST /api/v1/orders/checkout/

{
  "idempotency_key": "buyer1-checkout-0001"
}
```

The backend reserves stock inside a database transaction.

## Confirm demo payment

```http
POST /api/v1/orders/1/confirm-demo-payment/
```

This is a local demo payment only. It does not charge a card.

## Recommendations

```http
GET /api/v1/recommendations/
```

Anonymous users receive a popular-products fallback. Authenticated users receive a simple TF-IDF content-based recommendation result when interaction history exists.

---

# Important Production Notes

Before a real production deployment:

1. Replace demo payment confirmation with a provider sandbox and verified webhook.
2. Add payment webhook signature verification and event deduplication.
3. Add reservation expiry through Celery Beat.
4. Add Redis cache keys and explicit invalidation for catalog endpoints.
5. Add email verification and password reset.
6. Add seller approval workflow and stronger object-level permissions.
7. Add coupon, review, shipment and refund modules.
8. Add audit logs and request correlation IDs.
9. Run concurrency tests against PostgreSQL.
10. Set `DEBUG=False`, HTTPS, secure cookies and managed secrets.
11. Add CI/CD, linting, dependency scanning and backups.
12. Measure latency, error rate and recommendation metrics before making performance claims.
