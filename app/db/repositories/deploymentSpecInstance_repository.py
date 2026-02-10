# /******************************************************************
# © 2025-2026 Infosys Limited, Bangalore, India. All Rights Reserved.
# Infosys believes the information in this document is accurate as of its publication date;
# such information is subject to change without notice. Infosys acknowledges the proprietary
# rights of other companies to the trademarks, product names and such other intellectual property
# rights mentioned in this document. Except as expressly permitted, neither this documentation nor
# any part of it may be reproduced, stored in a retrieval system, or transmitted in any form or by
# any means, electronic, mechanical, printing, photocopying, recording or otherwise, without the prior
# permission of Infosys Limited and/or any named intellectual property rights holders under this document.
# *******************************************************************/

# PROPRIETARY NOTICE
# This software is confidential and proprietary information of Infosys Limited.
# You shall not disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into with Infosys Limited.

import logging
from typing import List
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.db.session import setup_database
from sqlalchemy.exc import SQLAlchemyError
from app.db.models.deploymentSpecInstance import deploymentSpecInstance
from app.schemas.deploymentSpecInstance import deploymentSpecInstanceCreate

logger = logging.getLogger(__name__)


def list_deploymentSpecInstance(
        db: Session, limit_: int) -> List[deploymentSpecInstance]:
    try:
        if not db:
            raise ValueError("Database session is None")
        if limit_ <= 0:
            raise ValueError("Limit must be a positive integer")

        result = db.execute(select(deploymentSpecInstance).order_by(
            deploymentSpecInstance.expName).limit(limit_))
        return list(result.scalars().all())
    except SQLAlchemyError as e:
        logger.error(f"Database error listing deployment spec instances: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error listing deployment spec instances: {e}")
        raise


def get_deployment_details(table_name: str, deployment_name: str):

    try:
        if not table_name:
            raise ValueError("Table name cannot be empty")
        if not deployment_name:
            raise ValueError("Deployment name cannot be empty")

        try:
            engine, SessionLocal, metadata = setup_database()
        except Exception as e:
            logger.error(f"DB initialization failed: {e}")
            raise

        # Table check
        if table_name not in metadata.tables:
            logger.error(f"Table '{table_name}' not found in the database.")
            raise KeyError(f"Table '{table_name}' not found in the database.")

        table = metadata.tables[table_name]

        try:
            conn = engine.connect()
            try:
                stmt = select(table).where(table.c.expName == deployment_name)
                result = conn.execute(stmt).fetchone()
            finally:
                conn.close()
        except SQLAlchemyError as e:
            logger.error(f"DB query failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during DB query: {e}")
            raise

        # Row not found
        if not result:
            logger.info(f"No deployment found with expName '{deployment_name}'")
            return None

        # Convert SQLAlchemy Row into dict
        try:
            columns = table.columns.keys()
            result_dict = dict(zip(columns, result))
        except Exception as e:
            logger.error(f"Error converting result to dictionary: {e}")
            raise

        return result_dict

    except Exception as e:
        logger.error(f"Error getting deployment details: {e}")
        raise


def add_deploymentSpecInstance_resource(
        db: Session, payload_list: deploymentSpecInstanceCreate, logger):
    try:
        if not db:
            raise ValueError("Database session is None")
        if not payload_list:
            raise ValueError("Payload list cannot be empty")
        if not isinstance(payload_list, list):
            raise TypeError("Payload must be a list")

        instances = []
        for item in payload_list:
            try:
                instance = deploymentSpecInstance(**item)
                instances.append(instance)
            except TypeError as e:
                raise TypeError(
                    f"Invalid data format for deployment spec instance: {e}")
            except Exception as e:
                raise Exception(f"Error creating deployment spec instance: {e}")

        try:
            db.add_all(instances)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Failed to commit deployment spec instances: {e}")
            raise

        try:
            for instance in instances:
                db.refresh(instance)
        except SQLAlchemyError as e:
            logger.warning(f"Failed to refresh instances: {e}")
            # Don't raise here as instances are already committed

        logger.info("Successfully added deploymentSpecInstance....!")
        return instances
    except Exception as e:
        logger.error(f"Error adding deployment spec resources: {e}")
        raise


def delete_deployment_from_db(table_name: str, deployment_name: str) -> bool:
    """
    Delete a deployment record from the DB.
    Returns True if a row was deleted, False if not found.
    """

    try:
        if not table_name:
            raise ValueError("Table name cannot be empty")
        if not deployment_name:
            raise ValueError("Deployment name cannot be empty")

        # Use your centralized DB setup function
        try:
            engine, SessionLocal, metadata = setup_database()
        except Exception as e:
            logger.error(f"DB initialization failed: {e}")
            raise

        if table_name not in metadata.tables:
            logger.error(f"Table '{table_name}' not found in DB.")
            raise KeyError(f"Table '{table_name}' not found in DB.")

        table = metadata.tables[table_name]

        # Check if record exists before deleting
        try:
            existing = get_deployment_details(table_name, deployment_name)
        except Exception as e:
            logger.error(f"Error checking for existing deployment: {e}")
            raise

        if not existing:
            logger.info(
                f"No deployment found with expName '{deployment_name}' to delete")
            return False

        try:
            stmt = delete(table).where(table.c.expName == deployment_name)
            with engine.connect() as conn:
                result = conn.execute(stmt)
                conn.commit()

            deleted = result.rowcount > 0
            if deleted:
                logger.info(
                    f"Successfully deleted deployment '{deployment_name}' from DB")
            return deleted
        except SQLAlchemyError as e:
            logger.error(f"DB deletion error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during deletion: {e}")
            raise

    except Exception as e:
        logger.error(f"Failed to delete deployment from DB: {e}")
        return False
