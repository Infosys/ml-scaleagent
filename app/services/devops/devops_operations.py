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
import yaml
import logging
import requests
from itertools import count
from app.config import settings
from app.db import check_required_tables
from urllib.parse import urlparse, parse_qs
from app.db.repositories.deploymentSpecInstance_repository import get_deployment_details

logger = logging.getLogger(__name__)


def pipelineRun_status(run_id: str):
    try:
        if not run_id:
            raise ValueError("Run ID cannot be empty")

        try:
            azure_devops_pat = settings["ado_config"]["AZURE_DEVOPS_PAT"]
            organization = settings["ado_config"]["ORGANIZATION"]
            project = settings["ado_config"]["PROJECT"]
            pipeline_name = settings["ado_config"]["PIPELINE_NAME"]
        except KeyError as e:
            msg = f"Missing required Azure DevOps configuration: {e}"
            raise KeyError(msg)

        if not all([azure_devops_pat, organization, project, pipeline_name]):
            msg = "One or more Azure DevOps configuration values are empty"
            raise ValueError(msg)

        pipelines_url = (
            f"https://dev.azure.com/{organization}/{project}"
            "/_apis/pipelines?api-version=7.1"
        )
        pipeline_id = None
        try:
            resp_pipe = requests.get(
                pipelines_url,
                auth=('', azure_devops_pat),
                timeout=20
            )
            resp_pipe.raise_for_status()

            data = resp_pipe.json()
            for p in data.get("value", []):
                if p.get("name") == pipeline_name:
                    pipeline_id = p.get("id")
                    break
            if not pipeline_id:
                msg = f"Pipeline '{pipeline_name}' not found in Azure DevOps."
                logger.error(msg)
                raise ValueError(f"Pipeline '{pipeline_name}' not found")
        except requests.exceptions.Timeout:
            logger.error("Request timeout while fetching pipeline ID")
            raise TimeoutError("Azure DevOps API request timed out")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise ConnectionError(f"Failed to connect to Azure DevOps: {e}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error fetching pipelines: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching pipeline_id: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error fetching pipeline_id: %s", e)
            raise

        status_url = (
            f"https://dev.azure.com/{organization}/{project}"
            f"/_apis/pipelines/{pipeline_id}/runs/{run_id}?api-version=7.1"
        )

        logger.info("\\n==== Pipeline Run Status (Ctrl+C to stop) ====\\n")

        last_state = None
        last_result = None
        build_id = None
        printed_counts = {}

        for _ in count():
            try:
                try:
                    resp_status = requests.get(
                        status_url,
                        auth=('', azure_devops_pat),
                        timeout=20
                    )
                    resp_status.raise_for_status()
                except requests.exceptions.Timeout:
                    logger.warning("Status check timed out, retrying...")
                    time.sleep(2)
                    continue
                except requests.exceptions.ConnectionError as e:
                    logger.warning(f"Connection error during status check: {e}")
                    time.sleep(2)
                    continue
                except requests.exceptions.HTTPError as e:
                    logger.error(f"HTTP error checking status: {e}")
                    return e.response.status_code
                except requests.exceptions.RequestException as e:
                    logger.error(f"Request error: {e}")
                    time.sleep(2)
                    continue

                if resp_status.ok:
                    try:
                        data = resp_status.json()
                    except ValueError as e:
                        logger.error(f"Invalid JSON response: {e}")
                        time.sleep(2)
                        continue

                    run_id_val = data.get("id")
                    state = data.get("state", "unknown")
                    result = data.get("result", "unknown")
                    url = data.get("_links", {}).get("web", {}).get("href", "")

                    if state != last_state or result != last_result:
                        last_state = state
                        last_result = result
                        logger.info(
                            "Run %s • State: %s • Result: %s",
                            run_id_val, state, result
                        )
                        if url:
                            logger.info("Run URL: %s", url)

                    # Try to stream live build logs if buildId is available in URL
                    if url and not build_id:
                        try:
                            q = parse_qs(urlparse(url).query)
                            build_id = q.get("buildId", [None])[0]
                            if build_id:
                                logger.info("Streaming logs for buildId: %s", build_id)
                        except Exception as e:
                            logger.debug("Unable to parse buildId from URL: %s", e)

                    if build_id:
                        try:
                            base = (
                                f"https://dev.azure.com/"
                                f"{organization}/{project}"
                            )
                            logs_index_url = (
                                f"{base}/_apis/build/builds/"
                                f"{build_id}/logs?api-version=7.1"
                            )

                            try:
                                resp_logs = requests.get(
                                    logs_index_url,
                                    auth=('', azure_devops_pat),
                                    timeout=20
                                )
                                resp_logs.raise_for_status()
                            except requests.exceptions.RequestException as e:
                                logger.debug(f"Failed to fetch build logs: {e}")
                                resp_logs = None

                            if resp_logs and resp_logs.ok:
                                try:
                                    logs = resp_logs.json().get('logs', [])
                                    for entry in logs:
                                        log_id = entry.get('id')
                                        if log_id is None:
                                            continue

                                        log_url = (
                                            f"{base}/_apis/build/builds/"
                                            f"{build_id}/logs/"
                                            f"{log_id}?api-version=7.1"
                                        )
                                        try:
                                            r = requests.get(
                                                log_url,
                                                auth=('', azure_devops_pat),
                                                timeout=20
                                            )
                                            if not r.ok:
                                                continue

                                            content = r.text or ""
                                            lines = content.splitlines()
                                            prev = printed_counts.get(log_id, 0)
                                            if prev < len(lines):
                                                for line in lines[prev:]:
                                                    if line.strip():
                                                        logger.info(line)
                                                printed_counts[log_id] = len(lines)
                                        except requests.exceptions.RequestException:
                                            continue
                                except (ValueError, KeyError) as e:
                                    logger.debug(f"Error parsing build logs: {e}")

                            # Fallback/augmentation: poll timeline
                            # and stream per-record logs
                            timeline_url = (
                                f"{base}/_apis/build/builds/"
                                f"{build_id}/timeline?api-version=7.1"
                            )
                            try:
                                resp_tl = requests.get(
                                    timeline_url,
                                    auth=('', azure_devops_pat),
                                    timeout=20
                                )
                                if resp_tl.ok:
                                    try:
                                        records = resp_tl.json().get('records', [])
                                        for rec in records:
                                            log_info = rec.get('log') or {}
                                            tl_log_id = log_info.get('id')
                                            if tl_log_id is None:
                                                continue
                                            tl_log_url = (
                                                f"{base}/_apis/build/builds/"
                                                f"{build_id}/logs/"
                                                f"{tl_log_id}?api-version=7.1"
                                            )
                                            try:
                                                rr = requests.get(
                                                    tl_log_url,
                                                    auth=('', azure_devops_pat),
                                                    timeout=20
                                                )
                                                if not rr.ok:
                                                    continue
                                                tcontent = rr.text or ""
                                                tlines = tcontent.splitlines()
                                                tprev = printed_counts.get(
                                                    tl_log_id, 0
                                                )
                                                if tprev < len(tlines):
                                                    for line in tlines[tprev:]:
                                                        if line.strip():
                                                            logger.info(line)
                                                    printed_counts[
                                                        tl_log_id
                                                    ] = len(tlines)
                                            except requests.exceptions.RequestException:
                                                continue
                                    except (ValueError, KeyError) as e:
                                        logger.debug(
                                            f"Error parsing timeline: {e}"
                                        )
                            except requests.exceptions.RequestException as e:
                                logger.debug(f"Failed to fetch timeline: {e}")
                        except Exception as e:
                            logger.debug("Log streaming error: %s", e)

                    if state == "completed":
                        logger.info(
                            "\\n==== Deployment Completed ====\\nResult: %s",
                            result
                        )
                        return 200

                else:
                    logger.error(
                        "Azure DevOps API error: %s", resp_status.status_code
                    )
                    return resp_status.status_code

            except KeyboardInterrupt:
                logger.info("Stopped by user.")
                return

            except Exception as e:
                logger.error("Error while polling run status: %s", e)
                time.sleep(2)
                continue

            time.sleep(2)

    except KeyboardInterrupt:
        logger.info("Stopped by user.")
        return
    except Exception as e:
        logger.error(f"Pipeline run status check failed: {e}")
        raise


def trigger_pipeline(deploymentName: str):
    try:
        if not deploymentName:
            raise ValueError("Deployment name cannot be empty")

        # Check if all required tables exist in the database
        try:
            check_required_tables()
        except Exception as e:
            logger.error(f"Required tables check failed: {e}")
            raise

        try:
            result_dict = get_deployment_details(
                settings["db_config"]["tablename"],
                deploymentName
            )
        except Exception as e:
            logger.error(f"Failed to get deployment details: {e}")
            raise

        if not result_dict:
            error_msg = f"No DB configuration found for '{deploymentName}'."
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info("DB configuration found and loaded successfully.")

        try:
            expName = result_dict.get("expName")
            expWorkflowPath = result_dict.get("expWorkflowPath")
            modelArtifact = result_dict.get("modelArtifact", {}) or {}
            modelName = modelArtifact.get("modelName", "")
            modelVersion = modelArtifact.get("modelVersion", "")

            logging_conf = result_dict.get("logging", {}) or {}
            EventHubBindings = result_dict.get("EventHubBindings", {}) or {}
            initialOffsetOptions = (
                result_dict.get("initialOffsetOptions", {}) or {}
            )
            env = result_dict.get("env", {}).get("dev", {}) or {}
            clientRetryOptions = (
                result_dict.get("clientRetryOptions", {}) or {}
            )
        except Exception as e:
            logger.error(f"Error extracting deployment configuration: {e}")
            raise

        try:
            yaml_dict = {
                "experimentName": expName,
                "initScript": expWorkflowPath,
                "modelArtifact": {
                    "modelName": modelName,
                    "version": modelVersion
                },
                "logging": {
                    "default": logging_conf.get("default", ""),
                    "Host.Results": logging_conf.get("HostResults", ""),
                    "Function": logging_conf.get("Function", ""),
                    "Host.Aggregator": logging_conf.get("HostAggregator", "")
                },
                "EventHubBindings": {
                    "prefetchCount": EventHubBindings.get(
                        "prefetchCount", ""
                    ),
                    "maxEventBatchSize": EventHubBindings.get(
                        "maxEventBatchSize", ""
                    ),
                    "batchCheckpointFrequency": EventHubBindings.get(
                        "batchCheckpointFrequency", ""
                    )
                },
                "initialOffsetOptions": {
                    "type": initialOffsetOptions.get("type", ""),
                    "enqueuedTimeUtc": initialOffsetOptions.get(
                        "enqueuedTimeUtc", ""
                    )
                },
                "dev": {
                    "environmentKey": env.get("environmentKey", ""),
                    "functionEnvBindings": {
                        "SrcEventHubNamespace": env.get(
                            "SrcEventHubNamespace", ""
                        ),
                        "SrcEventHubName": env.get("SrcEventHubName", ""),
                        "srcConsumerGroup": env.get("srcConsumerGroup", ""),
                        "SinkEventHubNamespace": env.get(
                            "SinkEventHubNamespace", ""
                        ),
                        "SinkEventHubName": env.get("SinkEventHubName", ""),
                        "deadLetterEventHubNamespace": env.get(
                            "deadLetterEventHubNamespace", ""
                        ),
                        "deadLetterEventHubName": env.get(
                            "deadLetterEventHubName", ""
                        ),
                        "AzureWebJobsStorageAccount": env.get(
                            "AzureWebJobsStorageAccount", ""
                        ),
                        "transportType": env.get("transportType", ""),
                        "cpuLimit": env.get("cpuLimit", ""),
                        "memoryLimit": env.get("memoryLimit", ""),
                        "minReplica": env.get("minReplica", ""),
                        "maxReplica": env.get("maxReplica", ""),
                    },
                    "clientRetryOptions": {
                        "mode": clientRetryOptions.get("mode", ""),
                        "tryTimeout": clientRetryOptions.get("tryTimeout", ""),
                        "delay": clientRetryOptions.get("delay", ""),
                        "maxDelay": clientRetryOptions.get("maxDelay", ""),
                        "maxRetries": clientRetryOptions.get("maxRetries", ""),
                    }
                }
            }
        except Exception as e:
            logger.error(f"Error creating YAML dictionary: {e}")
            raise

        logger.info("\n==== YAML Generated From DB ====\n")
        try:
            yaml_content = yaml.dump(
                yaml_dict, sort_keys=False, default_flow_style=False
            )
            logger.info(yaml_content)
        except yaml.YAMLError as e:
            logger.error(f"Error converting dict to YAML: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during YAML generation: {e}")
            raise

        try:
            organization = settings["ado_config"]["ORGANIZATION"]
            project = settings["ado_config"]["PROJECT"]
            azure_devops_pat = settings["ado_config"]["AZURE_DEVOPS_PAT"]
            pipeline_name = settings["ado_config"]["PIPELINE_NAME"]
            branch_name = settings["ado_config"]["BRANCH_NAME"]
        except KeyError as e:
            raise KeyError(f"Missing required Azure DevOps configuration: {e}")

        pipelines_url = (
            f"https://dev.azure.com/{organization}/{project}"
            "/_apis/pipelines?api-version=7.1"
        )
        pipeline_id = None

        try:
            try:
                resp_pipe = requests.get(
                    pipelines_url,
                    auth=('', azure_devops_pat),
                    timeout=20
                )
                resp_pipe.raise_for_status()
            except requests.exceptions.Timeout:
                msg = (
                    "Azure DevOps API request timed out "
                    "while fetching pipelines"
                )
                raise TimeoutError(msg)
            except requests.exceptions.ConnectionError as e:
                raise ConnectionError(f"Failed to connect to Azure DevOps: {e}")
            except requests.exceptions.HTTPError as e:
                raise Exception(f"HTTP error fetching pipelines: {e}")
            except requests.exceptions.RequestException as e:
                raise Exception(f"Error fetching pipelines: {e}")

            if resp_pipe.ok:
                try:
                    data = resp_pipe.json()
                    pipelines = data.get("value", [])

                    for p in pipelines:
                        if p.get("name") == pipeline_name:
                            pipeline_id = p.get("id")
                            break

                    if not pipeline_id:
                        error_msg = (
                            f"Pipeline '{pipeline_name}' "
                            "not found in Azure DevOps."
                        )
                        logger.error(error_msg)
                        raise ValueError(error_msg)
                except ValueError as e:
                    raise ValueError(f"Failed to parse Azure DevOps response: {e}")

            else:
                error_msg = f"Failed fetching pipelines: {resp_pipe.status_code}"
                logger.error(error_msg)
                raise Exception(error_msg)

        except Exception as e:
            logger.error(f"Error fetching pipeline ID: {e}")
            raise

        # ---- Trigger Pipeline ----
        pipeline_run_url = (
            f"https://dev.azure.com/{organization}/{project}/_apis/pipelines/"
            f"{pipeline_id}/runs?api-version=7.1"
        )

        payload = {
            "resources": {
                "repositories": {
                    "self": {
                        "refName": f"refs/heads/{branch_name}"
                    }
                }
            },
            "templateParameters": {
                "yamlConfig": yaml_content
            }
        }

        try:
            try:
                resp = requests.post(
                    pipeline_run_url,
                    auth=('', azure_devops_pat),
                    headers={"Content-Type": "application/json"},
                    json=payload,
                    timeout=30
                )
            except requests.exceptions.Timeout:
                raise TimeoutError("Pipeline trigger request timed out")
            except requests.exceptions.ConnectionError as e:
                raise ConnectionError(f"Failed to connect to Azure DevOps: {e}")
            except requests.exceptions.RequestException as e:
                raise Exception(f"Error triggering pipeline: {e}")

            if resp.ok:
                try:
                    result_info = resp.json()
                    run_id = result_info.get("id") or result_info.get(
                        "run_id"
                    )
                    logger.info(
                        f"Pipeline triggered successfully! Run ID: {run_id}"
                    )

                    msg = (
                        "Pipeline has been triggered succesfully. "
                        f"the run id is {run_id}"
                    )
                    logger.info(msg)
                    msg = (
                        "Please use the run id to trigger the "
                        "pipeline run status check."
                    )
                    logger.info(msg)
                    return {"status_code": resp.status_code, "run_id": run_id}
                except ValueError as e:
                    raise ValueError(f"Failed to parse pipeline trigger response: {e}")

            else:
                error_msg = f"Pipeline trigger failed: {resp.text[:500]}"
                logger.error(error_msg)
                return {"status_code": resp.status_code, "run_id": None}

        except Exception as ex:
            logger.error(f"Failed to reach Azure DevOps: {ex}")
            raise

    except Exception as e:
        logger.error(f"Pipeline trigger failed: {e}")
        raise
