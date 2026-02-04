import os
import yaml
import logging
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from app.config import settings

logger = logging.getLogger(__name__)


def setup_database():
    try:
        current_dir = os.path.dirname(__file__)
        app_dir = os.path.abspath(os.path.join(current_dir, '..'))
        config_path = os.path.join(app_dir, "config.yaml")

        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            if not config:
                raise ValueError("Configuration file is empty")
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at: {config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file: {e}")

        try:
            autocommit_val = config["db_config"]["autocommit"]
            autoflush_val = config["db_config"]["autoflush"]
            pool_pre_ping_val = config["db_config"]["pool_pre_ping"]
        except KeyError as e:
            raise KeyError(f"Missing required database configuration key: {e}")

        # Create engine
        try:
            db_url = settings["db_config"]["database_url"]
            if not db_url:
                raise ValueError("Database URL is empty or not configured")

            engine = create_engine(
                db_url,
                pool_pre_ping=pool_pre_ping_val
            )
        except KeyError:
            raise KeyError("Database URL not found in settings")
        except OperationalError as e:
            raise OperationalError(
                f"Failed to connect to database: {e}", params=None, orig=e.orig)
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Database engine creation failed: {e}")

        # Reflect metadata
        try:
            metadata = MetaData()
            metadata.reflect(bind=engine)
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Failed to reflect database metadata: {e}")

        # Build session factory
        try:
            SessionLocal = sessionmaker(
                autocommit=autocommit_val,
                autoflush=autoflush_val,
                bind=engine
            )
        except Exception as e:
            raise Exception(f"Failed to create session factory: {e}")

        return engine, SessionLocal, metadata

    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise


def check_required_tables():

    required_tables = [
        "computeInstance",
        "storageInstance",
        "eventSourceDefnInstance",
        "deploymentSpecInstance"
    ]

    try:
        # Create engine from database URL in settings
        try:
            db_url = settings["db_config"]["database_url"]
            if not db_url:
                raise ValueError("Database URL is not configured")
            engine = create_engine(db_url)
        except KeyError:
            raise KeyError("Database configuration not found in settings")
        except OperationalError as e:
            raise OperationalError(
                f"Failed to connect to database: {e}", params=None, orig=e.orig)
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Failed to create database engine: {e}")

        # Get inspector to check existing tables
        try:
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Failed to inspect database tables: {e}")
        except Exception as e:
            raise Exception(f"Error inspecting database: {e}")

        # Check for missing tables
        missing_tables = [
            table for table in required_tables
            if table not in existing_tables
        ]

        if missing_tables:
            error_message = (
                f"The following required table(s) are missing from the "
                f"database: {', '.join(missing_tables)}\n\n"
                f"Please add the required resources using:\n"
                f"  add-resource --help\n\n"
            )
            raise Exception(error_message)

        logger.info("All required tables exist in the database")
        return True

    except Exception as e:
        logger.error(f"Table check failed: {e}")
        if "required table(s) are missing" in str(e):
            raise
        else:
            raise Exception(
                f"Error checking database tables: {str(e)}\n\n"
                "Please ensure the database is properly configured and "
                "accessible.")


try:
    engine, SessionLocal, metadata = setup_database()
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    raise
