from .base import Base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import String


class ComputeInstance(Base):
    __tablename__ = "computeInstance"

    instanceName: Mapped[str] = mapped_column(String(255), primary_key=True)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    resourceFQDN: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resourceDNSPrefix: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resourceVersion: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    subscription: Mapped[str] = mapped_column(String(255), nullable=False)
    resourceGroup: Mapped[str] = mapped_column(String(255), nullable=False)
    environmentTag: Mapped[str | None] = mapped_column(String(255), nullable=True)
    instancePreference: Mapped[str] = mapped_column(
        String(255), nullable=False, default="default")
    resourceTags: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB), nullable=False, default=dict)
    agentPoolProfiles: Mapped[list] = mapped_column(
        MutableList.as_mutable(JSONB), nullable=False, default=list)
    resourceSpecInJSON: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB), nullable=False, default=dict)
