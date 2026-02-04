import logging
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.models.eventSourceDefnInstance import eventSourceDefnInstance
from app.schemas.eventSourceDefnInstance import eventSourceDefnInstanceCreate

logger = logging.getLogger(__name__)


def list_eventHub_Instance(db: Session, limit_: int) -> List[eventSourceDefnInstance]:
    try:
        if not db:
            raise ValueError("Database session is None")
        if limit_ <= 0:
            raise ValueError("Limit must be a positive integer")

        result = db.execute(select(eventSourceDefnInstance).order_by(
            eventSourceDefnInstance.EHName).limit(limit_))
        return list(result.scalars().all())
    except SQLAlchemyError as e:
        logger.error(f"Database error listing event hub instances: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error listing event hub instances: {e}")
        raise


def add_eventSourceDefnInstance_resource(
        db: Session, payload_list: eventSourceDefnInstanceCreate, logger):
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
                instance = eventSourceDefnInstance(**item)
                instances.append(instance)
            except TypeError as e:
                raise TypeError(f"Invalid data format for event source instance: {e}")
            except Exception as e:
                raise Exception(f"Error creating event source instance: {e}")

        try:
            db.add_all(instances)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Failed to commit event source instances: {e}")
            raise

        try:
            for instance in instances:
                db.refresh(instance)
        except SQLAlchemyError as e:
            logger.warning(f"Failed to refresh instances: {e}")
            # Don't raise here as instances are already committed

        logger.info("Successfully added EventHubInstance....!")
        return instances
    except Exception as e:
        logger.error(f"Error adding event source resources: {e}")
        raise
