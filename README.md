# StockSense — ready-to-run academic project

A Flask + PostgreSQL + Bootstrap retail inventory application with sales recording, low-stock alerts, a simple scikit-learn weekly demand forecast, reorder suggestions, automated tests, Docker and CI examples.

## Requirements
- Python 3.11+
- Docker Desktop (optional, for PostgreSQL/container run)
- Git (optional)

## Option A: Run locally with SQLite (quickest)
```bash
# Windows PowerShell
py -3.11 -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python -c "from app import app, db; app.app_context().push(); db.create_all()"
flask --app app seed
flask --app app run --debug
```
Open http://127.0.0.1:5000

On macOS/Linux, create/activate the environment with:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "from app import app, db; app.app_context().push(); db.create_all()"
flask --app app seed
flask --app app run --debug
```

## Option B: Run with PostgreSQL using Docker Compose
```bash
docker compose up --build
```
Open http://localhost:5000. The Compose file starts PostgreSQL and the web app. Demo data can be loaded in a second terminal:
```bash
docker compose exec web flask --app app seed
```
Stop with `docker compose down`. Add `-v` only if you intentionally want to delete the database volume.

## Tests
```bash
pytest --cov=app --cov=services --cov-report=term-missing
```

## Main pages
- `/` — dashboard and low-stock alerts
- `/products` — create, update and delete products
- `/sales` — record sales and update stock
- `/forecast` — next-week demand and suggested reorder quantity
- `/health` — deployment health check

## Forecast logic
Daily sale records are grouped into weekly totals. With at least three weekly buckets, linear regression estimates next-week demand. The page displays a simple holdout error estimate. Reorder suggestion is `max(0, forecast demand + reorder threshold - current stock)`. This is a teaching baseline, not a production-grade forecasting system.

## Project layout
```text
StockSense/
├── app.py, models.py, seed.py
├── services/                 # forecasting and reorder logic
├── templates/                # Bootstrap pages
├── static/css/
├── tests/                    # pytest tests
├── docs/                     # SRS, stories, test and SQA templates
├── .github/workflows/ci.yml
├── Dockerfile, docker-compose.yml, Jenkinsfile
└── requirements.txt
```

## Before submission / production
1. Change `SECRET_KEY` and PostgreSQL credentials.
2. Add authentication/authorization before exposing the app publicly.
3. Use database migrations (Flask-Migrate/Alembic) for schema changes.
4. Add a real PostgreSQL concurrency test and increase coverage to the course target (80%).
5. Evaluate forecast error on at least eight consecutive weeks of representative data. The handbook target is forecast error under 20%; this starter does not guarantee that target.
6. Add your team, institution, screenshots, interview notes, sprint evidence, GitHub URL and actual test results to the report and presentation. Do not submit sample/demo data as real interview evidence.
7. Forecasts are suggestions only; the shop owner decides orders.
