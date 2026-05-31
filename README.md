# DevOps Platform V2

A real-time DevOps e-commerce backend project using Flask, PostgreSQL, Docker, GitHub Actions, and Render.

## Features

- Flask REST API
- PostgreSQL database
- Docker containerization
- Docker Compose local setup
- GitHub Actions CI pipeline
- Pytest automated testing
- 77% test coverage
- Flake8 linting
- Bandit security scanning
- Gunicorn production server
- Render cloud deployment

## Architecture

Developer
→ GitHub
→ GitHub Actions
→ Tests, Linting, Security Scan
→ Docker Build
→ Render Deployment
→ Flask API
→ PostgreSQL

## API Endpoints

GET `/health`

GET `/db`

GET `/products`

GET `/products/<id>`

POST `/products`

PUT `/products/<id>`

DELETE `/products/<id>`

## Run Locally

```cmd
docker compose up --build -d