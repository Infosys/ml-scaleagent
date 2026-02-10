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


import json
import logging
import traceback
from sqlalchemy import update
from app.db.session import setup_database

from app.db.repositories.deploymentSpecInstance_repository import get_deployment_details

logger = logging.getLogger(__name__)


def apply_updates(
    table_name: str,
    deployment_name: str,
    update_items: list,
    overwrite: bool
):
    """
    Update deployment row using JSON patch-style logic.
    `overwrite` = True/False passed internally by CLI, not exposed to user.
    """
    try:
        # Validate inputs
        if not table_name:
            return False, "Table name cannot be empty"
        if not deployment_name:
            return False, "Deployment name cannot be empty"
        if not update_items:
            return False, "Update items cannot be empty"
        if not isinstance(update_items, list):
            return False, "Update items must be a list"

        try:
            engine, SessionLocal, metadata = setup_database()
        except Exception as e:
            logger.error(f"DB initialization failed: {e}")
            return False, f"DB initialization failed: {e}"

        if table_name not in metadata.tables:
            logger.error(f"Table '{table_name}' not found")
            return False, f"Table '{table_name}' not found."

        table = metadata.tables[table_name]
        try:
            existing = get_deployment_details(table_name, deployment_name)
        except Exception as e:
            logger.error(f"Failed to get deployment details: {e}")
            return False, f"Failed to retrieve deployment: {e}"

        if existing is None:
            return False, f"No deployment found with expName '{deployment_name}'."

        try:
            result_dict = existing.copy()
        except Exception as e:
            logger.error(f"Failed to copy deployment data: {e}")
            return False, f"Failed to process deployment data: {e}"

        top_level_updates = {}
        jsonb_updates = {}
        updated_pairs = []

        # -------- PROCESS UPDATE ITEMS --------
        try:
            for update_item in update_items:
                if not isinstance(update_item, dict):
                    return False, f"Invalid update format: {update_item}"

                for key, value in update_item.items():

                    if "." in key:
                        try:
                            col, *path = key.split(".")

                            current_json = result_dict.get(col)
                            if isinstance(current_json, str):
                                try:
                                    current_json = json.loads(current_json)
                                except json.JSONDecodeError as e:
                                    msg = (
                                        f"Failed to parse JSON for "
                                        f"column '{col}': {e}"
                                    )
                                    logger.warning(msg)
                                    current_json = {}
                                except Exception as e:
                                    msg = f"Unexpected error parsing JSON: {e}"
                                    logger.warning(msg)
                                    current_json = {}
                            if current_json is None:
                                current_json = {}

                            if col not in jsonb_updates:
                                jsonb_updates[col] = current_json

                            d = jsonb_updates[col]

                            for k in path[:-1]:
                                if k not in d or not isinstance(d[k], dict):
                                    if overwrite:
                                        d[k] = {}
                                    else:
                                        d = None
                                        break
                                if d:
                                    d = d[k]

                            if d:
                                d[path[-1]] = value
                                updated_pairs.append((key, value))
                        except Exception as e:
                            msg = (
                                f"Error processing nested update for "
                                f"key '{key}': {e}"
                            )
                            logger.error(msg)
                            return False, f"Failed to process update for '{key}': {e}"

                    else:
                        if (not overwrite) and (result_dict.get(key) is not None):
                            continue

                        top_level_updates[key] = value
                        updated_pairs.append((key, value))
        except Exception as e:
            logger.error(f"Error processing update items: {e}")
            return False, f"Failed to process updates: {e}"

        # ----- FINAL MERGE -----
        try:
            update_dict = top_level_updates.copy()
            for col, updated_json in jsonb_updates.items():
                update_dict[col] = updated_json
        except Exception as e:
            logger.error(f"Error merging updates: {e}")
            return False, f"Failed to merge updates: {e}"

        # ----- DB UPDATE -----
        try:
            conn = engine.connect()
            try:
                upd_stmt = (
                    update(table)
                    .where(table.c.expName == deployment_name)
                    .values(**update_dict)
                )
                conn.execute(upd_stmt)
                conn.commit()
            finally:
                conn.close()
        except Exception as e:
            logger.error(f"Database update failed: {e}")
            return False, f"Update failed: {e}"

        return True, updated_pairs
    except Exception as e:
        logger.error(f"Unexpected error in apply_updates: {e}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")
        return False, f"Unexpected error: {e}"
