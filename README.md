# ML-Scaler

A comprehensive ML deployment management system for Kubernetes-based machine learning model scaling and orchestration. ML-Scaler provides automated deployment, scaling, and lifecycle management for ML models on Azure Kubernetes Service (AKS) with Databricks integration.

## Features

- **Automated ML Model Deployment** - Deploy ML models to Kubernetes with automated configuration
- **Dynamic Scaling** - Auto-scale model deployments based on demand
- **Deployment Management** - List, update, and delete model deployments via API or CLI
- **Database Persistence** - Track deployment specs, compute instances, storage, and event sources
- **Databricks Integration** - Connect and manage Databricks workspaces for ML workflows
- **Azure DevOps Integration** - Trigger CI/CD pipelines for model deployments
- **RESTful API** - FastAPI-based REST endpoints for programmatic access
- **CLI Interface** - Typer-based command-line tool for operations

## Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- PostgreSQL database
- Databricks workspace and access token
- Azure Kubernetes Service (AKS) cluster
- Azure DevOps account (for pipeline integration)
- Azure Service Principal credentials

## Installation

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd ML-Scaler

# Start services
docker-compose up -d
```

### Local Installation

```bash
# Install dependencies
pip install -e .

# Set up environment variables (see Configuration)
cp env.example .env
# Edit .env with your configuration
```

## Configuration

### Security Setup

**IMPORTANT**: Never commit credentials to version control. Use environment variables for all sensitive data.

1. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

2. Configure required environment variables in `.env`:
   - **Database**: `DATABASE_URL`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
   - **Azure DevOps**: `AZURE_DEVOPS_PAT`, `ORGANIZATION`, `PROJECT`, `PIPELINE_NAME`
   - **Azure Service Principal**: `TENANT_ID`, `CLIENT_ID`, `CLIENT_SECRET`
   - **AKS**: `AKS_API_SERVER`, `NAMESPACE`

3. Update `app/config.yaml` with non-sensitive configuration:
   - Azure DevOps organization, project, pipeline, and branch names
   - AKS namespace (can also be set via environment)

4. **For Production**: Use Azure Key Vault or similar secret management service instead of `.env` files

## Usage

### API Server

```bash
# Using Docker
docker-compose up

# Or locally
uvicorn app.api.main:app --reload
```

API will be available at `http://localhost:8000`

### CLI Interface

```bash

#To see functionalities available

mlscaler --help

#Above command will guide you how to use defined cli commands 

## Architecture

- **FastAPI** - High-performance REST API framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Relational database for persistence
- **Typer** - Modern CLI framework
- **Kubernetes Client** - AKS cluster interaction
- **Azure DevOps API** - CI/CD pipeline orchestration

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## Contributing

Contributions are welcome! Please ensure:
- All tests pass
- Code follows project style guidelines
- Documentation is updated as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions, please open an issue in the repository.
