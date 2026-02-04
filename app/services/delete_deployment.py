import logging
from app.config import settings
from kubernetes.client.exceptions import ApiException
from app.services.aks_api_config import aks_api_config


logger = logging.getLogger(__name__)


def delete_deployment_from_aks(deployment_name):
    try:
        if not deployment_name:
            raise ValueError("Deployment name cannot be empty")

        # Get namespace from settings
        try:
            namespace_name = settings["aks_config"]["NAMESPACE"]
            if not namespace_name:
                raise ValueError("Namespace is not configured")
        except KeyError:
            raise KeyError("AKS namespace configuration not found")

        # Get AKS API clients
        try:
            apps_api, core_api = aks_api_config(silent=True)
        except Exception as e:
            logger.error(f"Failed to configure AKS API: {e}")
            raise

        # Delete the deployment
        try:
            apps_api.delete_namespaced_deployment(
                name=deployment_name,
                namespace=namespace_name
            )
            logger.info(
                f"Successfully deleted deployment '{deployment_name}' "
                f"from namespace '{namespace_name}'"
            )
            return 200
        except ApiException as e:
            if e.status == 404:
                msg = (
                    f"Deployment '{deployment_name}' not found "
                    f"in namespace '{namespace_name}'"
                )
                raise Exception(msg)
            elif e.status == 403:
                msg = (
                    "Access denied. Check service principal "
                    "permissions to delete deployments."
                )
                raise Exception(msg)
            else:
                raise ApiException(f"Failed to delete deployment: {e}")
        except Exception as e:
            raise Exception(f"Error deleting deployment '{deployment_name}': {e}")

    except Exception as e:
        logger.error(f"Failed to delete deployment from AKS: {e}")
        raise
