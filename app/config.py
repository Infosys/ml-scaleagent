import os
import yaml
import logging
from typing import ClassVar
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    config_path: ClassVar[str] = "./app/config.yaml"

    def configurations(self):
        try:
            # Load environment variables from .env file
            env_path = Path(__file__).resolve().parent.parent / ".env"
            try:
                load_dotenv(dotenv_path=env_path)
            except Exception as e:
                logger.warning(
                    f"Failed to load .env file: {e}. "
                    "Continuing with environment variables only.")

            # Load YAML configuration
            try:
                with open(self.config_path, "r") as f:
                    config = yaml.safe_load(f)
                if not config:
                    raise ValueError("Configuration file is empty or invalid")
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Configuration file not found at: {self.config_path}")
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid YAML format in configuration file: {e}")
            except Exception as e:
                raise Exception(f"Error reading configuration file: {e}")

            # Override sensitive values with environment variables
            try:
                if os.getenv("DATABASE_URL"):
                    config["db_config"]["database_url"] = os.getenv("DATABASE_URL")

                if os.getenv("AZURE_DEVOPS_PAT"):
                    config["ado_config"]["AZURE_DEVOPS_PAT"] = os.getenv(
                        "AZURE_DEVOPS_PAT")

                if os.getenv("TENANT_ID"):
                    config["service_principle_cred"]["TENANT_ID"] = os.getenv(
                        "TENANT_ID")

                if os.getenv("CLIENT_ID"):
                    config["service_principle_cred"]["CLIENT_ID"] = os.getenv(
                        "CLIENT_ID")

                if os.getenv("CLIENT_SECRET"):
                    config["service_principle_cred"]["CLIENT_SECRET"] = os.getenv(
                        "CLIENT_SECRET")
            except KeyError as e:
                raise KeyError(f"Missing required configuration key: {e}")

            return config
        except Exception as e:
            logger.error(f"Fatal error loading configuration: {e}")
            raise


try:
    settings_object = Settings()
    settings = settings_object.configurations()
except Exception as e:
    logger.error(f"Failed to initialize settings: {e}")
    raise
