from pydantic import BaseModel, Field
from typing_extensions import Literal
from typing import Optional, Dict, Any


class eventSourceDefnInstanceCreate(BaseModel):
    type: str
    provider: Literal["azure", "gcp", "aws"]
    EHName: str
    EHNameSpace: str
    consumerGroup: str
    consumerGroupStatus: str
    resourceSpecInJSON: Optional[Dict[str, Any]] = Field(default_factory=dict)
