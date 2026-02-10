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

import time
import logging
from app.config import settings
from prettytable import PrettyTable
from kubernetes.client.exceptions import ApiException
from app.services.aks_api_config import aks_api_config

# ANSI COLOR CODES
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

logger = logging.getLogger(__name__)


def list_deployments(silent=False, namespace_name=None):
    try:
        # Get namespace from settings
        try:
            NAMESPACE = settings["aks_config"]["NAMESPACE"]
            if not NAMESPACE:
                raise ValueError("Namespace is not configured")
        except KeyError:
            raise KeyError("AKS namespace configuration not found in settings")

        # Get AKS API clients
        try:
            apps_api, core_api = aks_api_config(silent=True)
        except Exception as e:
            logger.error(f"Failed to configure AKS API: {e}")
            raise

        # List deployments
        try:
            deployments = apps_api.list_namespaced_deployment(namespace=NAMESPACE)
        except ApiException as e:
            if e.status == 404:
                raise Exception(f"Namespace '{NAMESPACE}' not found")
            elif e.status == 403:
                msg = (
                    f"Access denied to namespace '{NAMESPACE}'. "
                    "Check service principal permissions."
                )
                raise Exception(msg)
            else:
                raise ApiException(f"Failed to list deployments: {e}")
        except Exception as e:
            raise Exception(f"Error listing deployments: {e}")

        if silent:
            return deployments.items

        if not deployments.items:
            logger.warning("No deployments found in the namespace.")
            return []

        # Display deployments in a formatted table
        logger.info(
            f"Found {len(deployments.items)} deployment(s) "
            f"in namespace '{NAMESPACE}':"
        )

        try:
            table = PrettyTable()
            table.field_names = [
                "Name", "Replicas", "Available", "Ready", "Age", "Status"
            ]
            table.align = "l"

            for dep in deployments.items:
                try:
                    name = dep.metadata.name
                    replicas = dep.spec.replicas or 0
                    available = dep.status.available_replicas or 0
                    ready = dep.status.ready_replicas or 0

                    # Calculate age
                    if dep.metadata.creation_timestamp:
                        try:
                            age = (
                                time.time()
                                - dep.metadata.creation_timestamp.timestamp()
                            )
                            days = int(age // 86400)
                            hours = int((age % 86400) // 3600)
                            minutes = int((age % 3600) // 60)

                            if days > 0:
                                age_str = f"{days}d {hours}h"
                            elif hours > 0:
                                age_str = f"{hours}h {minutes}m"
                            else:
                                age_str = f"{minutes}m"
                        except Exception as e:
                            logger.warning(
                                f"Failed to calculate age for "
                                f"deployment '{name}': {e}"
                            )
                            age_str = "Unknown"
                    else:
                        age_str = "Unknown"

                    # Determine status
                    state = "INACTIVE"
                    if dep.status.conditions:
                        for cond in dep.status.conditions:
                            if cond.type == "Available" and cond.status == "True":
                                state = "ACTIVE"
                                break

                    if state == "ACTIVE":
                        status_color = GREEN + "ACTIVE" + RESET
                    elif ready > 0:
                        status_color = YELLOW + "PARTIAL" + RESET
                    else:
                        status_color = RED + "INACTIVE" + RESET

                    table.add_row([
                        name, replicas, available, ready, age_str, status_color
                    ])
                except Exception as e:
                    logger.warning(f"Failed to process deployment info: {e}")
                    continue

            logger.info("\n%s", table)
        except Exception as e:
            logger.error(f"Error creating deployment table: {e}")
            # Still return items even if table creation fails

        return deployments.items

    except Exception as e:
        logger.error(f"Failed to list deployments: {e}")
        raise


def identify_deployment(aks_deployment_name: str, deployments):
    try:
        if not aks_deployment_name:
            raise ValueError("Deployment name cannot be empty")

        if not deployments:
            logger.warning("No deployments provided to search")
            return None

        matched_dep = next(
            (dep for dep in deployments if dep.metadata.name == aks_deployment_name),
            None
        )

        if not matched_dep:
            msg = f"Deployment '{aks_deployment_name}' not found in provided list"
            logger.debug(msg)
            return None

        return matched_dep

    except Exception as e:
        msg = f"Error identifying deployment '{aks_deployment_name}': {e}"
        logger.error(msg)
        return None
