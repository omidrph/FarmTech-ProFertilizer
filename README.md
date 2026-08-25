# 🌱 FarmTech — ProFertilizer

Intelligent fertilizer formulation and nutrient management platform for hydroponic and greenhouse cultivation.

## Overview

**FarmTech ProFertilizer** is a web-based platform for managing fertilizers, analyzing water and nutrient data, generating fertilizer formulations, and validating nutrient solutions.

The system is designed for greenhouse, hydroponic, and soilless cultivation workflows.

## Features

* Fertilizer management
* System and user-defined fertilizers
* Water analysis
* Nutrient target management
* Fertilizer formulation and optimization
* Non-Negative Least Squares (NNLS) optimization
* Nutrient balance validation
* Precipitation compatibility checks
* Reservoir calculation
* Recipe management
* Reports and calculation history
* User authentication and authorization
* Persian user interface
* RESTful API

## Technology Stack

| Layer                | Technology              |
| -------------------- | ----------------------- |
| Frontend             | Vue 3, TypeScript, Vite |
| Backend              | Python, FastAPI         |
| Database             | PostgreSQL              |
| ORM                  | SQLAlchemy              |
| Scientific Computing | NumPy, SciPy            |
| HTTP Client          | Axios                   |
| Containerization     | Docker, Docker Compose  |
| Reverse Proxy        | Traefik / Caddy         |

## Architecture

```text
Vue 3 Frontend
       │
       │ HTTPS / REST API
       ▼
FastAPI Backend
       │
       ├── Authentication
       ├── Fertilizer Management
       ├── Water Analysis
       ├── Recipe Management
       ├── Reports
       └── Optimization Engine
              │
              ├── NumPy
              └── SciPy / NNLS
       │
       ▼
PostgreSQL
```

## Optimization

The fertilizer optimization engine uses Non-Negative Least Squares (NNLS) to determine fertilizer quantities while preventing negative fertilizer amounts.

The optimization problem is formulated as:

```text
minimize ||Ax - b||²

subject to:

x ≥ 0
```

A simplified implementation:

```python
from scipy.optimize import nnls

weights, residual = nnls(A, b)
```

The calculation workflow generally consists of:

1. Processing water analysis
2. Calculating required nutrient concentrations
3. Subtracting nutrients already present in the water
4. Building the fertilizer matrix
5. Solving the NNLS optimization problem
6. Validating the resulting solution
7. Checking fertilizer compatibility
8. Generating the final formulation

## Project Structure

```text
FarmTech-ProFertilizer/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── models/
│   │   ├── services/
│   │   ├── seeds/
│   │   ├── middleware/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.*
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## Requirements

For local development:

* Python 3.11+
* Node.js 20+
* PostgreSQL 15+
* Docker and Docker Compose (recommended)

## Installation

Clone the repository:

```bash
git clone https://github.com/omidrph/FarmTech-ProFertilizer.git
cd FarmTech-ProFertilizer
```

Create the environment file:

```bash
cp .env.example .env
```

Configure the required environment variables in `.env`.

### Docker

Build and start the application:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Run the development server:

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

The exact configuration depends on the deployment environment.

Important variables include:

```env
DATABASE_URL=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

SECRET_KEY=

DEBUG=
ENVIRONMENT=

CORS_ORIGINS=

VITE_API_URL=
```

For production, sensitive values such as database passwords and `SECRET_KEY` must not be committed to Git.

## API

The backend exposes a versioned REST API under:

```text
/api/v1
```

Examples of available API areas include:

```text
/api/v1/auth
/api/v1/users
/api/v1/fertilizers
/api/v1/reports
/api/v1/calculations
```

The exact endpoints are defined by the backend routers.

## Production Deployment

The application can be deployed using Docker Compose behind a reverse proxy.

Recommended production flow:

```text
Internet
   │
   ▼
Cloudflare
   │ HTTPS
   ▼
Reverse Proxy
   │
   ├── Frontend
   │
   └── Backend
          │
          ▼
      PostgreSQL
```

The frontend and API should be served over HTTPS in production.

The frontend must not make HTTP API requests when the application itself is loaded over HTTPS. The API URL should therefore use an HTTPS URL or an appropriate same-origin configuration.

## Health Check

The backend provides:

```text
GET /health
```

A healthy response is:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

## Development

Run backend and frontend separately during development:

```bash
# Backend
cd backend
uvicorn app.main:app --reload
```

```bash
# Frontend
cd frontend
npm run dev
```

## Testing

Run the backend test suite with:

```bash
pytest
```

For Docker-based testing:

```bash
docker compose exec backend pytest
```

## Security

Production deployments should:

* Use HTTPS
* Store secrets in environment variables
* Use strong database credentials
* Restrict CORS origins
* Keep dependencies updated
* Avoid exposing PostgreSQL directly to the Internet
* Use secure authentication tokens
* Enable HTTPS-only communication between the browser and API

## License

Proprietary software © FarmTech.

Unauthorized copying, redistribution, or commercial use is prohibited unless explicitly permitted by the copyright holder.
