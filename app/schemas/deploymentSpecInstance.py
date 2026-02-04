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
