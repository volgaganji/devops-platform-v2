## CI/CD Pipeline

This project uses GitHub Actions to automatically:

- Install dependencies
- Run Flake8 linting
- Run Bandit security scan
- Run Pytest tests
- Build Docker image
- Push Docker image to Docker Hub
- Trigger Render deployment

## Docker Image

Docker Hub:

```cmd
docker pull volgaganji/devops-platform-v2:latest