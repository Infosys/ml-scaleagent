
from pathlib import Path
import sys
# Add project_root to Python path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
import json  # noqa: E402
import re as r  # noqa: E402
import time  # noqa: E402
import traceback  # noqa: E402
import logging  # noqa: E402
import typer  # noqa: E402
import urllib3  # noqa: E402
import yaml  # noqa: E402
from prettytable import PrettyTable  # noqa: E402
from rich import print as rprint  # noqa: E402
from app.config import settings  # noqa: E402
from app.db.models.base import Base  # noqa: E402
from app.db.session import (  # noqa: E402
    SessionLocal, engine)
from app.db.repositories.storage_repository import (  # noqa: E402
    list_storage_Instance,
    add_storage_resource
)
from app.db.repositories.compute_repository import (  # noqa: E402
    add_compute_resource)
from app.db.repositories.eventSourceDefnInstance_repository import (  # noqa: E402
    add_eventSourceDefnInstance_resource
)
from app.db.repositories.deploymentSpecInstance_repository import (  # noqa: E402
    get_deployment_details,
    add_deploymentSpecInstance_resource,
    delete_deployment_from_db
)
from app.db.update_db import apply_updates  # noqa: E402
from app.services.devops.devops_operations import (  # noqa: E402
    trigger_pipeline,
    pipelineRun_status
)
from app.services.list_deployments import (  # noqa: E402
    list_deployments, identify_deployment)
from app.services.delete_deployment import (  # noqa: E402
    delete_deployment_from_aks)
from startup import check_postgres_health  # noqa: E402


logging.getLogger("kubernetes").setLevel(logging.WARNING)
urllib3.disable_warnings()

# Initialize logger for this module
logger = logging.getLogger(__name__)

# ANSI COLOR CODES
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


app = typer.Typer(help="CLI interface to mlscaler agent.")


# ============= Config_Details ===============#

log_level_str = settings["logging"]["level"]
log_level = getattr(logging, log_level_str.upper())

# DB_URL = settings["db_config"]["database_url"]
TABLE_NAME = settings["db_config"]["tablename"]

# AZURE_DEVOPS_PAT = settings["ado_config"]["AZURE_DEVOPS_PAT"]
# ORGANIZATION = settings["ado_config"]["ORGANIZATION"]
# PROJECT = settings["ado_config"]["PROJECT"]
# PIPELINE_NAME = settings["ado_config"]["PIPELINE_NAME"]
# BRANCH_NAME = settings["ado_config"]["BRANCH_NAME"]


# =========================================#
logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


# ================ Functions_Used ===================#

def ensure_tables():
    """Ensure DB tables exist, with defensive error logging."""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        logger.error("Failed to ensure tables: %s", e)
        logger.debug("Traceback:\n%s", traceback.format_exc())
        raise


# ================== CLI_Methods ================ #


@app.command()
def initialize():
    """Initialize environment and optionally create storage resources."""
    try:
        logger.info("checking if all the  pre requisites are satisfied ....")
        ensure_tables()
        time.sleep(5)
        check_postgres_health()
        try:
            with SessionLocal() as db:
                list_storage_Instance(db, 10)
        except Exception as e:
            logger.error("Failed to list storage instances: %s", e)
            logger.debug("Traceback:\n%s", traceback.format_exc())
            raise typer.Exit(code=1)

        # if len(rows) == 0:
        #     logger.info(
        #         "No Storage Instance Found. creating the storage instance."
        #     )
        #     time.sleep(5)
        #     logger.info("Storage Instance created Successfully.")
        #     time.sleep(5)
        #     msg = (
        #         "Please add an existing storageInstanceSpec or new "
        #         "storage instance spec to be created ....."
        #     )
        #     logger.info(msg)
        #     rprint("Example (array):")
        #     rprint(json.dumps([
        #         {"name": "First item", "description": "Optional description"},
        #         {"name": "Second item"}
        #     ], indent=2))

        #     try:
        #         raw = typer.prompt("JSON")
        #     except (EOFError, KeyboardInterrupt):
        #         logger.warning("Input cancelled by user.")
        #         raise typer.Abort()

        #     try:
        #         payload = json.loads(raw)
        #         time.sleep(5)
        #         with SessionLocal() as db:
        #             add_storage_resource(db, payload, logger)
        #     except json.JSONDecodeError as e:
        #         rprint(f"[red]Invalid JSON: {e}[/red]")
        #         logger.debug("Invalid JSON input: %s", raw)
        #         raise typer.Abort()
        #     except Exception as e:
        #         logger.error("Failed to add storage resource: %s", e)
        #         logger.debug("Traceback:\n%s", traceback.format_exc())
        #         raise typer.Exit(code=1)
        # else:
        #     msg = (
        #         "intialization is completed. "
        #         "please proceed with the next command"
        #     )
        #     logger.info(msg)

        # logger.info(
        #     "eventSourceDefnInstance initialization is complete ...."
        # )
        # time.sleep(5)  # sleep interval for demo. To be removed.
        # logger.info("ComputeInstance initialization is complete ....")
        # time.sleep(5)  # sleep interval for demo. To be removed.
        # msg = (
        #     "All intialization is complete. "
        #     "please proceed with the next command"
        # )
        # logger.info(msg)
    except typer.Abort:
        # Preserve abort semantics
        raise
    except KeyboardInterrupt:
        logger.warning("Interrupted by user.")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error("An unexpected error occurred in 'initialize': %s", e)
        logger.debug("Traceback:\n%s", traceback.format_exc())
        raise typer.Exit(code=1)


@app.command("add-resource")
def add_resource(
    resource_type: str = typer.Option(
        "storageInstance",
        "--resource-type",
        help=(
            "Which Resource to add: storageInstance, "
            "eventSourceDefnInstance, computeInstance, "
            "deploymentSpecInstance"
        )
    )
):
    """command for adding a resource to cloud"""
    try:
        ensure_tables()
        time.sleep(5)

        if not isinstance(resource_type, str):
            logger.error("resource_type must be a string.")
            raise typer.Exit(code=1)
        rprint("Example (array):")
        rprint(json.dumps([
            {"name": "First item", "description": "Optional description"},
            {"name": "Second item"}
        ], indent=2))
        try:
            raw = typer.prompt("JSON")
        except (EOFError, KeyboardInterrupt):
            logger.warning("Input cancelled by user.")
            raise typer.Abort()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as e:
            rprint(f"[red]Invalid JSON: {e}[/red]")
            logger.debug("Invalid JSON input: %s", raw)
            raise typer.Abort()
        try:
            with SessionLocal() as db:
                if resource_type == "storageInstance":
                    time.sleep(5)
                    add_storage_resource(db, payload, logger)
                    logger.info("Storage resource(s) added successfully!")
                elif resource_type == "computeInstance":
                    time.sleep(5)
                    add_compute_resource(db, payload, logger)
                    logger.info("Compute resource(s) added successfully!")
                elif resource_type == "eventSourceDefnInstance":
                    time.sleep(5)
                    add_eventSourceDefnInstance_resource(db, payload, logger)
                    msg = (
                        "eventSourceDefnInstance resource(s) "
                        "added successfully!"
                    )
                    logger.info(msg)
                elif resource_type == "deploymentSpecInstance":
                    time.sleep(5)
                    add_deploymentSpecInstance_resource(db, payload, logger)
                    msg = (
                        "deploymentSpecInstance resource(s) "
                        "added successfully!"
                    )
                    logger.info(msg)
                else:
                    msg = (
                        "We only support creating resources : compute, "
                        "storage, eventSource & deploymentSpec"
                    )
                    logger.info(msg)

        except Exception as e:
            logger.error(
                "Failed to add resource for type '%s': %s",
                resource_type, e
            )
            logger.debug("Traceback:\n%s", traceback.format_exc())
            raise typer.Exit(code=1)
    except typer.Abort:
        raise
    except KeyboardInterrupt:
        logger.warning("Interrupted by user.")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error("An unexpected error occurred in 'add_resource': %s", e)
        logger.debug("Traceback:\n%s", traceback.format_exc())
        raise typer.Exit(code=1)


@app.command("list-deployments")
def list_deployments_cli():
    """
    Lists deployments in the configured AKS Namespace.
    """
    try:
        list_deployments()
    except Exception as e:
        logger.error(f"Failed to list deployments: {e}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")
        rprint(f"[red]Error: Failed to list deployments - {e}[/red]")
        raise typer.Exit(code=1)


@app.command("delete-deployment")
def delete_deployment_cli(
    deployment_name: str = typer.Option(
        ..., "--deployment-name",
        help="Name of the deployment to be deleted...."
    )
):
    """Delete deployment for particular deployment details."""
    try:
        if not deployment_name:
            rprint("[red]Error: Deployment name cannot be empty[/red]")
            raise typer.Exit(code=1)

        logger.info(f"Processing deployment: {deployment_name}")

        try:
            clean = deployment_name.replace(" ", "-").replace("_", "-")
            clean = r.sub(r"[^a-zA-Z0-9\\-]", "", clean).lower()
            aks_deployment_name = f"function-app-{clean}"
        except Exception as e:
            logger.error(f"Error normalizing deployment name: {e}")
            rprint(f"[red]Error: Failed to process deployment name - {e}[/red]")
            raise typer.Exit(code=1)

        logger.info(f"Normalized AKS deployment name → {aks_deployment_name}")

        try:
            logger.info("Fetching deployments from AKS…")
            deployments = list_deployments(silent=True)
            deployment_names = [d.metadata.name for d in deployments]

            logger.info(f"AKS deployments: {deployment_names}")
            in_aks = aks_deployment_name in deployment_names

        except Exception as e:
            logger.error(f"Error fetching AKS deployments: {e}")
            logger.debug(f"Traceback:\n{traceback.format_exc()}")
            rprint(f"[red]Error: Failed to fetch AKS deployments - {e}[/red]")
            in_aks = False

        delete_aks = False
        aks_deleted = False
        db_deleted = False

        if in_aks:
            logger.info(f"Deployment found in AKS: {aks_deployment_name}")

            try:
                msg = (
                    f"Do you want to delete '{aks_deployment_name}' "
                    "from AKS? (yes/no): "
                )
                confirm_aks = input(msg).strip().lower()
            except (EOFError, KeyboardInterrupt):
                logger.warning("User cancelled operation")
                rprint("\n[yellow]Operation cancelled by user[/yellow]")
                raise typer.Exit(code=0)

            delete_aks = confirm_aks in ("yes", "y")

            if delete_aks:
                logger.info(f"Deleting '{aks_deployment_name}' from AKS…")
                try:
                    delete_deployment_from_aks(aks_deployment_name)
                    logger.info("Successfully deleted from AKS.")
                    aks_deleted = True
                except Exception as e:
                    logger.error(f"Failed to delete from AKS: {e}")
                    logger.debug(f"Traceback:\n{traceback.format_exc()}")
                    rprint(f"[red]Warning: Failed to delete from AKS - {e}[/red]")
            else:
                logger.info("Skipped AKS deletion.")

        else:
            msg = (
                f"No AKS deployment found "
                f"named '{aks_deployment_name}'."
            )
            logger.warning(msg)

        try:
            msg = (
                f"Do you want to delete DB config for '{deployment_name}' "
                f"from table '{TABLE_NAME}'? (yes/no): "
            )
            confirm_db = input(msg).strip().lower()
        except (EOFError, KeyboardInterrupt):
            logger.warning("User cancelled operation")
            rprint("\n[yellow]Operation cancelled by user[/yellow]")
            raise typer.Exit(code=0)

        delete_db = confirm_db in ("yes", "y")

        if delete_db:
            logger.info("Deleting configuration from DB…")

            try:
                deleted = delete_deployment_from_db(TABLE_NAME, deployment_name)

                if deleted:
                    logger.info("DB record deleted.")
                    db_deleted = True
                else:
                    logger.warning(f"No DB record found for '{deployment_name}'.")
            except Exception as e:
                logger.error(f"Failed to delete from DB: {e}")
                logger.debug(f"Traceback:\n{traceback.format_exc()}")
                rprint(f"[red]Warning: Failed to delete from DB - {e}[/red]")
        else:
            logger.info("Skipped DB deletion.")

        if aks_deleted or db_deleted:
            logger.info("Delete operation completed successfully.")
        else:
            msg = (
                "No resources were deleted "
                "(AKS not deleted and DB unchanged)."
            )
            logger.info(msg)

    except typer.Exit:
        raise
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        rprint("\n[yellow]Operation interrupted by user[/yellow]")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error in delete_deployment: {e}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")
        rprint(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command("create-deployment")
def create_deployment(
    deployment_name: str = typer.Option(
        ..., "--deployment-name", help="Name of the deployment to update"
    ),
    overwrite_deployment: bool = typer.Option(
        False,
        "--overwrite-deployment",
        help="If True, Will overwrite existing deployment."
    )
):
    """Create deployment for particular deployment details."""
    try:
        if not deployment_name:
            rprint("[red]Error: Deployment name cannot be empty[/red]")
            raise typer.Exit(code=1)

        if overwrite_deployment:
            rprint("[yellow]--overwrite-deployment=True provided[/yellow]")

            # Normalize deployment name to AKS format
            try:
                kebab = deployment_name.replace(" ", "-").replace("_", "-")
                kebab = r.sub(r'[^a-zA-Z0-9\-]', '', kebab).lower()
                aks_deployment_name = f"function-app-{kebab}"
            except Exception as e:
                logger.error(f"Error normalizing deployment name: {e}")
                rprint(f"[red]Error: Failed to process deployment name - {e}[/red]")
                raise typer.Exit(code=1)

            # Check if deployment exists in AKS
            try:
                rprint("[green]Checking if deployment exists in AKS...[/green]")
                deployments = list_deployments(silent=True)
                deployment_found = None
                for dep in deployments:
                    if dep.metadata.name == aks_deployment_name:
                        deployment_found = dep
                        break
            except Exception as e:
                logger.error(f"Failed to list deployments: {e}")
                logger.debug(f"Traceback:\n{traceback.format_exc()}")
                rprint(f"[red]Error: Failed to check existing deployments - {e}[/red]")
                raise typer.Exit(code=1)

            if deployment_found:
                # Deployment exists, ask for confirmation
                msg = (
                    f"[yellow]Deployment '{aks_deployment_name}' "
                    "exists in AKS.[/yellow]"
                )
                rprint(msg)
                try:
                    msg = (
                        "Deployment exist, Do you want to "
                        "overwrite existing deployment?"
                    )
                    confirm_overwrite = typer.confirm(msg, default=False)
                except (EOFError, KeyboardInterrupt):
                    logger.warning("User cancelled operation")
                    rprint("\n[yellow]Operation cancelled by user[/yellow]")
                    raise typer.Exit(code=0)

                if not confirm_overwrite:
                    rprint("[red]Operation cancelled by user.[/red]")
                    raise typer.Exit(code=0)

                # User confirmed, trigger pipeline
                rprint("[green]Triggering pipeline to overwrite deployment...[/green]")
                try:
                    result = trigger_pipeline(deployment_name)
                except Exception as e:
                    logger.error(f"Failed to trigger pipeline: {e}")
                    logger.debug(f"Traceback:\n{traceback.format_exc()}")
                    rprint(f"[red]Error: Failed to trigger pipeline - {e}[/red]")
                    raise typer.Exit(code=1)

                run_id = result.get("run_id") if isinstance(result, dict) else None
                if run_id:
                    try:
                        msg = "Do you want to see pipeline Run Status?"
                        view_status = typer.confirm(msg, default=True)
                        if view_status:
                            pipelineRun_status(str(run_id))
                    except Exception as e:
                        logger.error(f"Error checking pipeline status: {e}")
                        msg = (
                            "[yellow]Warning: Could not retrieve "
                            f"pipeline status - {e}[/yellow]"
                        )
                        rprint(msg)
                else:
                    logger.warning("No run_id returned from pipeline trigger.")
                return result
            else:
                # Deployment does not exist
                rprint("[red]Deployment does not exist in AKS.[/red]")
                rprint(
                    "[yellow]Please use below command to "
                    "create deployment:[/yellow]"
                )
                msg = (
                    '[green]create-deployment --deployment-name '
                    f'"{deployment_name}"[/green]'
                )
                rprint(msg)
                raise typer.Exit(code=1)

        try:
            kebab = deployment_name.replace(" ", "-").replace("_", "-")
            kebab = r.sub(r'[^a-zA-Z0-9\-]', '', kebab).lower()
            aks_deployment_name = f"function-app-{kebab}"
        except Exception as e:
            logger.error(f"Error normalizing deployment name: {e}")
            rprint(f"[red]Error: Failed to process deployment name - {e}[/red]")
            raise typer.Exit(code=1)

        try:
            deployments = list_deployments(silent=True)
        except Exception as e:
            logger.error(f"Failed to list deployments: {e}")
            logger.debug(f"Traceback:\n{traceback.format_exc()}")
            rprint(f"[red]Error: Failed to check existing deployments - {e}[/red]")
            raise typer.Exit(code=1)

        rprint("\n[bold]Checking for existing deployment...[/bold]\n")

        try:
            deployment_found = None
            for dep in deployments:
                if dep.metadata.name == aks_deployment_name:
                    deployment_found = dep
                    break
        except Exception as e:
            logger.error(f"Error searching for deployment: {e}")
            rprint(f"[red]Error: Failed to search deployments - {e}[/red]")
            raise typer.Exit(code=1)

        if deployment_found:
            msg = (
                f"[yellow]Deployment '{aks_deployment_name}' "
                "already exists in AKS.[/yellow]\n"
            )
            rprint(msg)
            rprint("\nTo overwrite the existing deployment, use:")
            msg = (
                f'[green]create-deployment --deployment-name '
                f'"{deployment_name}" --overwrite-deployment[/green]\n'
            )
            rprint(msg)
            return

        try:
            msg = (
                f"No deployment found with '{deployment_name}'."
                "\nDo you want to deploy the model?"
            )
            user_decision = typer.confirm(msg, default=False)
        except (EOFError, KeyboardInterrupt):
            logger.warning("User cancelled operation")
            rprint("\n[yellow]Operation cancelled by user[/yellow]")
            raise typer.Exit(code=0)

        if not user_decision:
            rprint("[red]Operation cancelled by user.[/red]")
            raise typer.Exit(code=0)

        rprint("[green]Proceeding to DB validation...[/green]")

        # Trigger deployment pipeline
        try:
            result = trigger_pipeline(deployment_name)
        except Exception as e:
            logger.error(f"Failed to trigger pipeline: {e}")
            logger.debug(f"Traceback:\n{traceback.format_exc()}")
            rprint(f"[red]Error: Failed to trigger pipeline - {e}[/red]")
            raise typer.Exit(code=1)

        run_id = result.get("run_id") if isinstance(result, dict) else None
        if run_id:
            try:
                msg = "Do you want to see pipeline Run Status?"
                view_status = typer.confirm(msg, default=True)
                if view_status:
                    pipelineRun_status(str(run_id))
            except Exception as e:
                logger.error(f"Error checking pipeline status: {e}")
                msg = (
                    "[yellow]Warning: Could not retrieve "
                    f"pipeline status - {e}[/yellow]"
                )
                rprint(msg)
        else:
            logger.warning("No run_id returned from pipeline trigger.")

    except typer.Exit:
        raise
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        rprint("\n[yellow]Operation interrupted by user[/yellow]")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error in create_deployment: {e}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")
        rprint(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command("update-deployment")
def update_deployment(
    deployment_name: str = typer.Option(..., "--deployment-name"),
    overwrite_deployment: bool = typer.Option(
        True,
        "--overwrite-deployment",
        help="Overwrite existing keys or not."
    )
):
    """Update existing deployment details"""
    try:
        if not deployment_name:
            rprint("[red]Error: Deployment name cannot be empty[/red]")
            raise typer.Exit(code=1)

        try:
            deployment_data = get_deployment_details(TABLE_NAME, deployment_name)
        except Exception as e:
            logger.error(f"Failed to get deployment details: {e}")
            logger.debug(f"Traceback:\n{traceback.format_exc()}")
            rprint(f"[red]Error: Failed to retrieve deployment - {e}[/red]")
            raise typer.Exit(code=1)

        if deployment_data is None:
            rprint(f"[red]No deployment found with expName '{deployment_name}'.[/red]")
            return

        rprint(f"[yellow]Deployment '{deployment_name}' found.[/yellow]")
        rprint(
            "[bold]Enter updates as JSON list:[/bold]\n"
            '[ {"env.dev.cpuLimit": "3000m"}, {"expDesc": "New description"} ]'
        )

        try:
            updates = input("\nEnter your updates as JSON: ").strip()
        except (EOFError, KeyboardInterrupt):
            logger.warning("User cancelled operation")
            rprint("\n[yellow]Operation cancelled by user[/yellow]")
            raise typer.Exit(code=0)

        if not updates:
            rprint("[red]No updates provided.[/red]")
            return

        try:
            update_items = json.loads(updates)
            if not isinstance(update_items, list):
                raise ValueError("Update must be list of dict")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {e}")
            rprint(f"[red]Invalid JSON: {e}[/red]")
            return
        except Exception as e:
            logger.error(f"Error parsing updates: {e}")
            rprint(f"[red]Invalid JSON: {e}[/red]")
            return

        try:
            success, msg = apply_updates(
                TABLE_NAME,
                deployment_name,
                update_items,
                overwrite_deployment
            )
        except Exception as e:
            logger.error(f"Failed to apply updates: {e}")
            logger.debug(f"Traceback:\n{traceback.format_exc()}")
            rprint(f"[red]Error: Failed to update deployment - {e}[/red]")
            raise typer.Exit(code=1)

        if not success:
            rprint(f"[red]{msg}[/red]")
            return

        try:
            updated_str = ", ".join(f"{k}={v}" for k, v in msg)
            rprint(f"[green]Updated successfully: {updated_str}[/green]\n")
        except Exception as e:
            logger.warning(f"Error formatting update message: {e}")
            rprint("[green]Updated successfully[/green]\n")

        try:
            user_choice = input("Trigger deployment now? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            logger.warning("User cancelled operation")
            rprint("\n[yellow]Operation cancelled by user[/yellow]")
            return

        if user_choice in ("y", "yes"):
            try:
                result = trigger_pipeline(deployment_name)
            except Exception as e:
                logger.error(f"Failed to trigger pipeline: {e}")
                logger.debug(f"Traceback:\n{traceback.format_exc()}")
                rprint(f"[red]Error: Failed to trigger pipeline - {e}[/red]")
                return

            run_id = result.get("run_id") if isinstance(result, dict) else None
            if run_id:
                try:
                    msg = "Do you want to see pipeline Run Status?"
                    view_status = typer.confirm(msg, default=True)
                    if view_status:
                        pipelineRun_status(str(run_id))
                except Exception as e:
                    logger.error(f"Error checking pipeline status: {e}")
                    msg = (
                        "[yellow]Warning: Could not retrieve "
                        f"pipeline status - {e}[/yellow]"
                    )
                    rprint(msg)
            else:
                logger.warning("No run_id returned from pipeline trigger.")

    except typer.Exit:
        raise
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        rprint("\n[yellow]Operation interrupted by user[/yellow]")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error in update_deployment: {e}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")
        rprint(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command("view-deployment")
def view_deployment(
    deployment_name: str = typer.Option(
        ..., "--deployment-name", help="Name of the deployment to view"
    )
):
    """
    View deployment details & AKS Status.
    """
    try:
        if not deployment_name:
            rprint("[red]Error: Deployment name cannot be empty[/red]")
            raise typer.Exit(code=1)

        rprint("[bold]Checking deployment in DB...[/bold]")

        try:
            result_dict = get_deployment_details(TABLE_NAME, deployment_name)
        except Exception as e:
            logger.error(f"Failed to get deployment details: {e}")
            logger.debug(f"Traceback:\n{traceback.format_exc()}")
            rprint(f"[red]Error: Failed to retrieve deployment from DB - {e}[/red]")
            result_dict = None

        if not result_dict:
            msg = (
                "[bold red]Deployment details not found in DB "
                f"for '{deployment_name}'.[/bold red]"
            )
            rprint(msg)
            rprint(
                "[yellow]Use the command below to "
                "add configuration:[/yellow]"
            )
            rprint("[bold cyan]add-resource --help[/bold cyan]\n")
        else:
            rprint("[green]✓ DB configuration found[/green]")

            rprint("\n[bold]DB Configuration (YAML):[/bold]")

            try:
                yaml_str = yaml.dump(
                    {str(k): v for k, v in result_dict.items()},
                    sort_keys=False,
                    default_flow_style=False
                )
                rprint(f"[cyan]{yaml_str}[/cyan]")
            except Exception as e:
                logger.error(f"Failed to format deployment data as YAML: {e}")
                msg = (
                    "[yellow]Warning: Could not format "
                    f"configuration as YAML - {e}[/yellow]"
                )
                rprint(msg)

        try:
            kebab = deployment_name.replace(" ", "-").replace("_", "-")
            kebab = r.sub(r"[^a-zA-Z0-9\-]", "", kebab).lower()
            aks_deployment_name = f"function-app-{kebab}"
        except Exception as e:
            logger.error(f"Error normalizing deployment name: {e}")
            rprint(f"[red]Error: Failed to process deployment name - {e}[/red]")
            raise typer.Exit(code=1)

        try:
            deployments = list_deployments(silent=True)
        except Exception as e:
            logger.error(f"Failed to list deployments: {e}")
            logger.debug(f"Traceback:\n{traceback.format_exc()}")
            rprint(f"[red]Error: Failed to check AKS deployments - {e}[/red]")
            return

        rprint("[bold]Checking AKS for deployment...[/bold]\n")

        try:
            deployment_found = None
            for dep in deployments:
                if dep.metadata.name == aks_deployment_name:
                    deployment_found = dep
                    break
        except Exception as e:
            logger.error(f"Error searching deployments: {e}")
            rprint(f"[red]Error: Failed to search deployments - {e}[/red]")
            return

        if deployment_found:
            msg = (
                "[green]✓ Deployment found in AKS: "
                f"{aks_deployment_name}[/green]\n"
            )
            rprint(msg)

            try:
                ready = deployment_found.status.ready_replicas or 0
                replicas = deployment_found.spec.replicas or 0
                status = (
                    "[green]ACTIVE[/green]"
                    if ready == replicas else
                    "[yellow]PARTIAL[/yellow]"
                )

                rprint(
                    f"Name: [cyan]{deployment_found.metadata.name}[/cyan] | "
                    f"Replicas: [cyan]{replicas}[/cyan] | "
                    f"Ready: [cyan]{ready}[/cyan] | "
                    f"Status: {status}\n"
                )
            except Exception as e:
                logger.error(f"Error extracting deployment details: {e}")
                msg = (
                    "[yellow]Warning: Could not extract all "
                    f"deployment details - {e}[/yellow]"
                )
                rprint(msg)

        else:
            msg = (
                f"[red]✘ Deployment '{aks_deployment_name}' "
                "not found in AKS.[/red]"
            )
            rprint(msg)

        return

    except typer.Exit:
        raise
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        rprint("\n[yellow]Operation interrupted by user[/yellow]")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error in view_deployment: {e}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")
        rprint(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command("check-deployment-status")
def check_deployment_status(
    deployment_name: str = typer.Option(
        ...,
        "--deployment-name",
        help="Name of the deployment to check"
    )
):
    """Check status for a specific AKS deployment."""
    try:
        if not deployment_name:
            rprint("[red]Error: Deployment name cannot be empty[/red]")
            raise typer.Exit(code=1)

        try:
            kebab = deployment_name.replace(" ", "-").replace("_", "-")
            kebab = r.sub(r'[^a-zA-Z0-9\-]', '', kebab).lower()
            aks_deployment_name = f"function-app-{kebab}"
        except Exception as e:
            logger.error(f"Error normalizing deployment name: {e}")
            rprint(f"[red]Error: Failed to process deployment name - {e}[/red]")
            raise typer.Exit(code=1)

        msg = (
            "\n[bold]Checking deployment status for: "
            f"'{aks_deployment_name}'[/bold]\n"
        )
        rprint(msg)

        try:
            deployments = list_deployments(silent=True)
        except Exception as e:
            logger.error(f"Failed to list deployments: {e}")
            logger.debug(f"Traceback:\n{traceback.format_exc()}")
            rprint(f"[red]Error: Failed to list deployments - {e}[/red]")
            raise typer.Exit(code=1)

        try:
            matched_dep = identify_deployment(aks_deployment_name, deployments)
        except Exception as e:
            logger.error(f"Error identifying deployment: {e}")
            rprint(f"[red]Error: Failed to identify deployment - {e}[/red]")
            raise typer.Exit(code=1)

        if not matched_dep:
            msg = f"[red]Deployment '{aks_deployment_name}' not found.[/red]"
            rprint(msg)
            rprint("\nTo list all deployments, use:")
            rprint("[yellow]list-deployments[/yellow]\n")
            return

        try:
            replicas = matched_dep.spec.replicas or 0
            ready = matched_dep.status.ready_replicas or 0
            available = matched_dep.status.available_replicas or 0

            state = "INACTIVE"
            if matched_dep.status.conditions:
                for cond in matched_dep.status.conditions:
                    if cond.type == "Available" and cond.status == "True":
                        state = "ACTIVE"
                        break

            if state == "ACTIVE":
                status_color = GREEN + "ACTIVE" + RESET
            elif ready > 0:
                status_color = YELLOW + "PARTIAL" + RESET
            else:
                status_color = RED + "INACTIVE" + RESET
        except Exception as e:
            logger.error(f"Error extracting deployment details: {e}")
            msg = (
                "[red]Error: Failed to extract "
                f"deployment status - {e}[/red]"
            )
            rprint(msg)
            raise typer.Exit(code=1)

        try:
            table = PrettyTable()
            table.field_names = [
                "Deployment", "Replicas", "Ready", "Available", "Status"
            ]
            table.align = "l"

            table.add_row([
                matched_dep.metadata.name,
                replicas,
                ready,
                available,
                status_color
            ])

            logger.info("\n" + str(table))
        except Exception as e:
            logger.error(f"Error creating status table: {e}")
            rprint("[yellow]Warning: Could not create formatted table[/yellow]")
            rprint(f"Deployment: {matched_dep.metadata.name}")
            msg = (
                f"Replicas: {replicas}, Ready: {ready}, "
                f"Available: {available}"
            )
            rprint(msg)
            rprint(f"Status: {state}")

    except typer.Exit:
        raise
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        rprint("\n[yellow]Operation interrupted by user[/yellow]")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"Unexpected error in check_deployment_status: {e}")
        logger.debug(f"Traceback:\n{traceback.format_exc()}")
        rprint(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        logger.warning("Interrupted by user at top-level.")
        raise typer.Exit(code=1)
