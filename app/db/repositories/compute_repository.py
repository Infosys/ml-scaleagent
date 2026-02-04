import logging
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.models.computeinstance import ComputeInstance
from app.schemas.computeInstance import computeInstanceCreate

logger = logging.getLogger(__name__)


def list_compute_Instance(db: Session, limit_: int) -> List[ComputeInstance]:
    try:
        if not db:
            raise ValueError("Database session is None")
        if limit_ <= 0:
            raise ValueError("Limit must be a positive integer")

        result = db.execute(select(ComputeInstance).order_by(
            ComputeInstance.instanceName).limit(limit_))
        return list(result.scalars().all())
    except SQLAlchemyError as e:
        logger.error(f"Database error listing compute instances: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error listing compute instances: {e}")
        raise


def add_compute_resource(db: Session, payload_list: computeInstanceCreate, logger):
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
                instance = ComputeInstance(**item)
                instances.append(instance)
            except TypeError as e:
                raise TypeError(f"Invalid data format for compute instance: {e}")
            except Exception as e:
                raise Exception(f"Error creating compute instance: {e}")

        try:
            db.add_all(instances)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Failed to commit compute instances: {e}")
            raise

        try:
            for instance in instances:
                db.refresh(instance)
        except SQLAlchemyError as e:
            logger.warning(f"Failed to refresh instances: {e}")
            # Don't raise here as instances are already committed

        logger.info("Successfully added computeInstances....!")
        return instances
    except Exception as e:
        logger.error(f"Error adding compute resources: {e}")
        raise
