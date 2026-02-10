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
