from pydantic import BaseModel, Field
from typing_extensions import Literal
from typing import Optional, Dict, Any


class storageInstanceCreate(BaseModel):
    type: str
    provider: Literal["azure", "gcp", "aws"]
    instanceName: str
    location: str
    subscription: str
    resourceGroup: str
    resourceFQDN: Optional[str] = None
    resourceDNSPrefix: Optional[str] = None
    environmentTag: Optional[str] = None
    instancePreference: str = Field(default="default")
    resourceTags: Optional[Dict[str, str]] = Field(default_factory=dict)
    resourceSpecInJSON: Optional[Dict[str, Any]] = Field(default_factory=dict)
