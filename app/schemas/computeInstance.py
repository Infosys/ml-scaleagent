from pydantic import BaseModel, Field
from typing_extensions import Literal
from typing import Optional, Dict, List, Any


class computeInstanceCreate(BaseModel):
    type: str
    provider: Literal["azure", "gcp", "aws"]
    instanceName: str
    resourceFQDN: Optional[str] = None
    resourceDNSPrefix: Optional[str] = None
    resourceVersion: str
    location: str
    subscription: str
    resourceGroup: str
    environmentTag: Optional[str] = None
    instancePreference: str = Field(default="default")
    resourceTags: Optional[Dict[str, str]] = Field(default_factory=dict)
    agentPoolProfiles: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    resourceSpecInJSON: Optional[Dict[str, Any]] = Field(default_factory=dict)
