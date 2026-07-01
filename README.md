# Soko Bora 🌽 — Fair Market Prices for Every Farmer

**Tagline:** *Know your market before you sell.*

## Problem Statement

Smallholder farmers across East Africa frequently sell their produce at
whatever price the nearest buyer offers, because they have no easy way to
compare prices across nearby markets. Middlemen often exploit this
information gap, buying low from farmers who don't know that a market
30km away is paying significantly more for the same crop. Soko Bora
("good market" in Swahili) closes that information gap by letting
farmers, buyers, and field agents report and view real-time crop prices
across markets in their region.

## Target Users

- **Smallholder farmers** deciding where and when to sell their harvest
- **Buyers/traders** wanting visibility into fair regional pricing
- **Agricultural extension workers / NGOs** monitoring price trends to
  support farmer cooperatives

## Core Features

1. **Submit price reports** — any user can report a crop price observed
   at a specific market (crop, market, region, price per kg)
2. **Browse current prices** — view all reported prices, most recent first
3. **Filter by crop or region** — quickly compare, e.g., maize prices
   across all markets in Kigali
4. *(Planned — F2/F3)* Price trend charts over time per crop/region
5. *(Planned — F2/F3)* SMS/USSD access for farmers without smartphones

## Technology Stack

- **Backend:** Python 3.11, Flask, Flask-SQLAlchemy
- **Database:** PostgreSQL (production/Docker), SQLite (local/tests)
- **Testing:** pytest
- **Linting:** flake8
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- *(Planned — later formatives)* Terraform for IaC, monitoring stack,
  microservices split (e.g., separating price-ingestion from
  price-query services)

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   └── main.py              # Flask app, models, and routes
├── tests/
│   ├── __init__.py
│   └── test_main.py         # pytest test suite
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Running Locally with Docker Compose (recommended)

The whole stack — app + PostgreSQL — starts with a single command:

```bash
docker-compose up --build
```

This builds the app image from the `Dockerfile`, starts a PostgreSQL
container, and connects them over an internal Docker network. The API
will be available at **http://localhost:5000**.

Stop everything with:

```bash
docker-compose down
```

To also wipe the persisted database volume:

```bash
docker-compose down -v
```

## Running Locally without Docker

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
python app/main.py
```

Without Docker, the app defaults to a local SQLite file
(`soko_bora.db`) unless you set a `DATABASE_URL` environment variable
pointing at a PostgreSQL instance.

The API will be available at `http://localhost:5000`.

### Example usage

```bash
# Report a price
curl -X POST http://localhost:5000/api/prices \
  -H "Content-Type: application/json" \
  -d '{"crop_name": "Maize", "market_name": "Kimironko Market", "region": "Kigali", "price_per_kg": 350, "reported_by": "farmer_jane"}'

# List all prices
curl http://localhost:5000/api/prices

# Filter by region
curl "http://localhost:5000/api/prices?region=Kigali"
```

## Running Tests

```bash
pytest tests/ -v
flake8 app tests --max-line-length=100
```

## CI Pipeline

The pipeline (`.github/workflows/ci.yml`) triggers on:
- Pushes to any branch **except** `main`
- Pull requests targeting `main`

Steps, in order:
1. Checkout code
2. Set up Python 3.11
3. Install dependencies
4. Lint with flake8 (**fails the build on lint errors**)
5. Run tests with pytest, using an in-memory SQLite DB (**fails the
   build on any test failure**)
6. Build the Docker image (**fails the build if the image doesn't
   build**)
7. Spin up a real Postgres container and smoke-test the built image
   against it by hitting `/health`

## Branch Protection

`main` requires the CI check (`Lint, Test, and Build Docker Image`) to
pass before a pull request can be merged. Configured under
**Settings → Branches → Branch protection rules** on GitHub.


## Project Board

See the GitHub Projects Kanban board linked in the repository description
for the current backlog, in-progress work, and completed items. See
`PROJECT_BOARD.md` in this repo for the initial backlog content used to
seed that board.