from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import String, Text


class deploymentSpecInstance(Base):
    __tablename__ = "deploymentSpecInstance"

    expName: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False)
    expType: Mapped[str] = mapped_column(String(255), nullable=False)
    expDesc: Mapped[str] = mapped_column(Text, nullable=False)
    expWorkflowPath: Mapped[str] = mapped_column(String(255), nullable=False)
    expRequirementsPath: Mapped[str] = mapped_column(String(255), nullable=False)
    modelArtifact: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB),
        nullable=False,
        default=lambda: {
            "type": "",
            "modelName": "",
            "modelVersion": "",
            "modelDescMetadata": "",
            "artifactPath": "",
            "storageType": ""
        }
    )
    logging: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB),
        nullable=False,
        default=lambda: {
            "HostResults": "",
            "Function": "",
            "HostAggregator": ""
        }
    )
    EventHubBindings: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB),
        nullable=False,
        default=lambda: {
            "prefetchCount": 0,
            "maxEventBatchSize": 0,
            "batchCheckpointFrequency": 0
        }
    )
    initialOffsetOptions: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB),
        nullable=False,
        default=lambda: {
            "type": "",
            "enqueuedTimeUtc": ""
        }
    )
    env: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB),
        nullable=False,
        default=lambda: {
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
    clientRetryOptions: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB),
        nullable=False,
        default=lambda: {
            "mode": "",
            "tryTimeout": "",
            "delay": "",
            "maxDelay": "",
            "maxRetries": 0
        }
    )
