import logging
from sqlalchemy.orm import Session
from app.db.models.base import Base
from app.schemas.item import ItemRead
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
from app.db.session import engine, SessionLocal
from fastapi import FastAPI, Depends, HTTPException
from app.db.repositories.item_repository import list_items


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting application and creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        yield
    except SQLAlchemyError as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        raise
    finally:
        logger.info("Application shutdown")

app = FastAPI(title="FastAPI + SQLAlchemy + Postgres + CLI", lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()


@app.get("/items", response_model=list[ItemRead])
def get_items(db: Session = Depends(get_db)):
    try:
        items = list_items(db)
        return items
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching items: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error while fetching items: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
