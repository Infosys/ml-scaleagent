from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.db.models.item import Item

logger = logging.getLogger(__name__)


def list_items(db: Session, limit_: int = 100) -> List[Item]:
    try:
        if not db:
            raise ValueError("Database session is None")
        if limit_ <= 0:
            raise ValueError("Limit must be a positive integer")

        result = db.execute(select(Item).order_by(Item.id).limit(limit_))
        return list(result.scalars().all())
    except SQLAlchemyError as e:
        logger.error(f"Database error listing items: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error listing items: {e}")
        raise


def seed_items(db: Session, count: int = 3) -> int:
    try:
        if not db:
            raise ValueError("Database session is None")
        if count <= 0:
            raise ValueError("Count must be a positive integer")

        to_add = [
            Item(name=f"Item {i+1}", description=f"Seeded item #{i+1}")
            for i in range(count)
        ]

        try:
            db.add_all(to_add)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Failed to seed items: {e}")
            raise

        return len(to_add)
    except Exception as e:
        logger.error(f"Error seeding items: {e}")
        raise
