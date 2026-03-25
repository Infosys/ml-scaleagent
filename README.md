
# ML-Scaler

A comprehensive ML deployment management system for Kubernetes-based machine learning model scaling and orchestration. ML-Scaler provides automated deployment, scaling, and lifecycle management for ML models on Azure Kubernetes Service (AKS) with Databricks integration.

## Features

- **Automated ML Model Deployment** - Deploy ML models to Kubernetes with automated configuration
- **Dynamic Scaling** - Auto-scale model deployments based on demand
- **Deployment Management** - List, update, and delete model deployments via CLI
- **Database Persistence** - Track deployment specs, compute instances, storage, and event sources
- **Databricks Integration** - Connect and manage Databricks workspaces for ML workflows
- **Azure DevOps Integration** - Trigger CI/CD pipelines for model deployments
- **CLI Interface** - Typer-based command-line tool for operations

## Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- PostgreSQL database
- Databricks workspace and access token
- Azure Kubernetes Service (AKS) cluster
- Azure DevOps account (for pipeline integration)
- Azure Service Principal credentials

## Quick Start Guide

### Installation

#### Using Docker Compose (Recommended)

Using a Docker Compose file along with a local environment file and configuration YAML values will bring the CLI wrapper up and running.

```bash
# Clone the repository
git clone <repository-url>
cd <directory>

# Start services
docker-compose up -d
```

#### Local Installation

```bash
# Install dependencies
pip install -e .

# Set up environment variables (see Configuration)
cp env.example .env
# Edit .env with your configuration
```

### Configuration

#### Security Setup

**IMPORTANT**: Never commit credentials to version control. Use environment variables for all sensitive data.

1. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

2. Configure required environment variables in `.env`:
   - **Database**: `DATABASE_URL`
   - **Azure DevOps**: `AZURE_DEVOPS_PAT`
   - **Azure Service Principal**: `TENANT_ID`, `CLIENT_ID`, `CLIENT_SECRET`
   - **Azure Databricks Configurations**: `DATABRICKS_HOST`, `DATABRICKS_TOKEN`

3. Update `app/config.yaml` with non-sensitive configuration:
   - Azure DevOps organization, project, pipeline, and branch name
   - AKS api_server & namespace 
   - You can also handle the logging_level, db_config non-sensitive informations accordingly.  

## NOTE:----> You can set the configurations either in ".env" file or  "app/config.yaml" accordingly based on sensitivity.

4. **For Production**: Use Azure Key Vault or similar secret management service instead of `.env` files


### CLI Interface


**CLI commands offered by mlscaler:**

`mlscaler --help`


[ABOVE COMMAND WILL GUIDE YOU HOW TO USE DEFINED CLI COMMANDS]

<img width="1593" height="537" alt="image" src="https://github.com/user-attachments/assets/b329ee5b-ace7-4382-a29a-6089e99ce441" />


#### `initialize`
Initialize environment, check DB health, and ensure required tables are present.

<img width="1918" height="163" alt="image" src="https://github.com/user-attachments/assets/d9fc2cd3-d943-4e96-8d5f-45f6b9715eb3" />


#### `add-resource`
Add configuration for required instance resources (storage, compute, event source, deployment spec) to DB.

<img width="1917" height="703" alt="image" src="https://github.com/user-attachments/assets/799419c0-e7d0-45a5-99c0-e9944c2f539d" />


#### `create-deployment --deployment-name <name>`
Trigger deployment for a specific deployment name. Checks AKS for existing deployment first. Use `--overwrite-deployment` flag if deployment already exists.
It has provision to check the pipeline status as well.

<img width="1911" height="203" alt="image" src="https://github.com/user-attachments/assets/1b5fbb7b-7362-4a99-bd96-ebf330d58e33" />
<img width="1905" height="139" alt="image" src="https://github.com/user-attachments/assets/d4693a57-fafb-4c7f-8271-529c22aa01ab" />
<img width="1903" height="70" alt="image" src="https://github.com/user-attachments/assets/03a3aab8-484d-40ba-9ec5-46681df998b3" />


#### `update-deployment --deployment-name <name>`
Update configuration key-values for a deployment in DB. On user confirmation, triggers pipeline with updated configurations.
On trigger, it has provision to check the pipeline status as well.

<img width="1918" height="315" alt="image" src="https://github.com/user-attachments/assets/d9e35f21-3763-4237-ba27-98b0da45b155" />


#### `view-deployment --deployment-name <name>`
View DB configurations and AKS deployment details for a specific deployment.
<img width="1733" height="526" alt="image" src="https://github.com/user-attachments/assets/f31a0452-d150-4035-91d8-a651654e50d4" />
<img width="1914" height="190" alt="image" src="https://github.com/user-attachments/assets/e1be76a0-965b-4135-9b03-9e2d8ee81115" />


#### `list-deployments`
List all deployments available in AKS under the configured namespace.

<img width="1915" height="382" alt="image" src="https://github.com/user-attachments/assets/34b4768b-da27-40de-abf4-5fd98c84b812" />


#### `check-deployment-status --deployment-name <name>`
Check deployment status in AKS for a specific deployment.
<img width="1909" height="384" alt="image" src="https://github.com/user-attachments/assets/1e74c7e8-11f5-497f-9fbc-31dbbf80f126" />


#### `delete-deployment --deployment-name <name>`
Delete deployment from AKS and DB configuration on user confirmation.
<img width="1894" height="610" alt="image" src="https://github.com/user-attachments/assets/0725711d-4f15-46cc-acca-896472bb3c18" />


## Architecture

- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Relational database for persistence
- **Typer** - Modern CLI framework
- **Kubernetes Client** - AKS cluster interaction
- **Azure DevOps API** - CI/CD pipeline orchestration

## Code Quality

This project follows Python best practices and PEP 8 guidelines. Future versions may include automated testing.

## Subscription-Based Offerings

ML-Scaler functionalities are also available through subscription-based platforms:

- **ChatBot Integration** - Access ML-Scaler features through an intelligent conversational interface


<img width="1396" height="516" alt="image" src="https://github.com/user-attachments/assets/b23be0a3-b5b0-477f-a1c1-adf8ffed5c2a" />

- **de.ai Platform by Infosys** - Enterprise-grade implementation of ML-Scaler with enhanced features and support.

<img width="832" height="880" alt="image" src="https://github.com/user-attachments/assets/c1ab789f-fbc7-4dee-8927-2f76bf2b828f" />


<img width="820" height="790" alt="image" src="https://github.com/user-attachments/assets/c73afc1d-81b7-473d-a3bc-1bb81562140b" />

For subscription details and platform access, please contact our team.

## Contributing

Contributions are welcome! Please ensure:
- Code follows project style guidelines
- Documentation is updated as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions, please open an issue in the repository.
