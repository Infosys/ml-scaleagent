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

from pydantic import BaseModel, Field
from typing import Dict, Any


class deploymentSpecInstanceCreate(BaseModel):
    expName: str
    expType: str
    expDesc: str
    expWorkflowPath: str
    expRequirementsPath: str
    modelArtifact: Dict[str, Any] = Field(
        default_factory=lambda: {
            "type": "",
            "modelName": "",
            "modelVersion": "",
            "modelDescMetadata": "",
            "artifactPath": "",
            "storageType": ""
        }
    )
    logging: Dict[str, Any] = Field(
        default_factory=lambda: {
            "HostResults": "",
            "Function": "",
            "HostAggregator": ""
        }
    )
    EventHubBindings: Dict[str, Any] = Field(
        default_factory=lambda: {
            "prefetchCount": 0,
            "maxEventBatchSize": 0,
            "batchCheckpointFrequency": 0
        }
    )
    initialOffsetOptions: Dict[str, Any] = Field(
        default_factory=lambda: {
            "type": "",
            "enqueuedTimeUtc": ""
        }
    )
    env: Dict[str, Dict[str, Any]] = Field(
        default_factory=lambda: {
            "dev": {
                "SrcEventHubName": "",
                "SrcEventHubNamespace": "",
                "SrcEventHubConnString": "",
                "srcConsumerGroup": "",
                "SinkEventHubNamespace": "",
                "deadLetterEventHubNamespace": "",
                "deadLetterEventHubName": "",
                "deadLetterEventHubConnString": "",
                "AzureWebJobsStorageAccount": "",
                "AzureWebJobsStorage": "",
                "transportType": "",
                "cpuLimit": "",
                "memoryLimit": "",
                "minReplica": 0,
                "maxReplica": 0
            },
            "qa": {
                "SrcEventHubName": "",
                "SrcEventHubNamespace": "",
                "SrcEventHubConnString": "",
                "srcConsumerGroup": "",
                "SinkEventHubNamespace": "",
                "deadLetterEventHubNamespace": "",
                "deadLetterEventHubName": "",
                "deadLetterEventHubConnString": "",
                "AzureWebJobsStorageAccount": "",
                "AzureWebJobsStorage": "",
                "transportType": "",
                "cpuLimit": "",
                "memoryLimit": "",
                "minReplica": 0,
                "maxReplica": 0
            }
        }
    )
    clientRetryOptions: Dict[str, Any] = Field(
        default_factory=lambda: {
            "mode": "",
            "tryTimeout": "",
            "delay": "",
            "maxDelay": "",
            "maxRetries": 0
        }
    )
