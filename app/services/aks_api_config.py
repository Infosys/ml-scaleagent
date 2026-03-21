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

import requests
import logging
from kubernetes import client
from app.config import settings
from kubernetes.client import ApiClient
from kubernetes.client.exceptions import ApiException


# ANSI COLOR CODES
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

logger = logging.getLogger(__name__)


def aks_api_config(silent=False):
    try:
        # Retrieve credentials from settings
        try:
            TENANT_ID = settings["service_principle_cred"]["TENANT_ID"]
            CLIENT_ID = settings["service_principle_cred"]["CLIENT_ID"]
            CLIENT_SECRET = settings["service_principle_cred"]["CLIENT_SECRET"]
            AKS_API_SERVER = settings["aks_config"]["AKS_API_SERVER"]
        except KeyError as e:
            raise KeyError(f"Missing required configuration key: {e}")

        # Validate credentials
        if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET, AKS_API_SERVER]):
            msg = (
                "One or more Azure credentials are empty "
                "or not configured"
            )
            raise ValueError(msg)

        if not silent:
            logger.info("Authenticating with Azure AD…")

        token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials",
            "scope": "6dae42f8-4368-4678-94ff-3960e28e3630/.default"
        }

        try:
            token_response = requests.post(token_url, data=payload, timeout=30)
            token_response.raise_for_status()
            token_data = token_response.json()

            if "access_token" not in token_data:
                raise ValueError("Access token not found in Azure AD response")

            token = token_data["access_token"]
        except requests.exceptions.Timeout:
            raise TimeoutError("Azure AD authentication request timed out")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Azure AD: {e}")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Azure AD authentication failed with HTTP error: {e}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Azure AD authentication request failed: {e}")
        except ValueError as e:
            raise ValueError(f"Failed to parse Azure AD response: {e}")

        if not silent:
            logger.info("Token acquired successfully!")

        try:
            configuration = client.Configuration()
            configuration.host = AKS_API_SERVER
            configuration.verify_ssl = True
            configuration.api_key = {"authorization": f"Bearer {token}"}

            api_client = ApiClient(configuration)
            apps_api = client.AppsV1Api(api_client)
            core_api = client.CoreV1Api(api_client)
        except ApiException as e:
            raise ApiException(f"Failed to configure Kubernetes API client: {e}")
        except Exception as e:
            raise Exception(f"Error creating Kubernetes API clients: {e}")

        return apps_api, core_api

    except Exception as e:
        logger.error(f"AKS API configuration failed: {e}")
        raise
