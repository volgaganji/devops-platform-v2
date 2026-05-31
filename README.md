\# DevOps Platform V2



\## Features

\- Flask REST API

\- PostgreSQL Database

\- Docker

\- Docker Compose

\- GitHub Actions CI/CD

\- Pytest Testing

\- Flake8 Linting

\- Bandit Security Scan

\- Render Deployment



\## Endpoints



GET /health

GET /products

POST /products

PUT /products/<id>

DELETE /products/<id>



\## Run Locally



docker compose up --build



\## Run Tests



pytest tests/



\## CI/CD



GitHub Actions automatically runs:

\- Linting

\- Security Scan

\- Tests

\- Docker Build

