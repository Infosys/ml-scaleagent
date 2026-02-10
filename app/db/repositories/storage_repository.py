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
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.models.storageInstance import StorageInstance
from app.schemas.storageInstance import storageInstanceCreate

logger = logging.getLogger(__name__)


def list_storage_Instance(db: Session, limit_: int) -> List[StorageInstance]:
    try:
        if not db:
            raise ValueError("Database session is None")
        if limit_ <= 0:
            raise ValueError("Limit must be a positive integer")

        result = db.execute(select(StorageInstance).order_by(
            StorageInstance.instanceName).limit(limit_))
        return list(result.scalars().all())
    except SQLAlchemyError as e:
        logger.error(f"Database error listing storage instances: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error listing storage instances: {e}")
        raise


def add_storage_resource(db: Session, payload_list: storageInstanceCreate, logger):
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
                instance = StorageInstance(**item)
                instances.append(instance)
            except TypeError as e:
                raise TypeError(f"Invalid data format for storage instance: {e}")
            except Exception as e:
                raise Exception(f"Error creating storage instance: {e}")

        try:
            db.add_all(instances)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Failed to commit storage instances: {e}")
            raise

        try:
            for instance in instances:
                db.refresh(instance)
        except SQLAlchemyError as e:
            logger.warning(f"Failed to refresh instances: {e}")
            # Don't raise here as instances are already committed

        logger.info("Successfully added storageInstances.")
        return instances
    except Exception as e:
        logger.error(f"Error adding storage resources: {e}")
        raise

# def add_storage_resource(db: Session, payload: storageInstanceCreate, logger):
#     storage_instance_obj = StorageInstance(**payload.dict())
#     db.add(storage_instance_obj)
#     db.commit()
#     db.refresh(storage_instance_obj)
#     logger.info(
#         f"Successfully added the StorageInstance: "
#         f"{storage_instance_obj.instanceName}")
#     return "200"
