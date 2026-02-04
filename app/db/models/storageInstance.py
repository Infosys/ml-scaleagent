from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import String

from .base import Base


class StorageInstance(Base):
    __tablename__ = "storageInstance"

    instanceName: Mapped[str] = mapped_column(String(255), primary_key=True)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    subscription: Mapped[str] = mapped_column(String(255), nullable=False)
    resourceGroup: Mapped[str] = mapped_column(String(255), nullable=False)
    resourceFQDN: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resourceDNSPrefix: Mapped[str | None] = mapped_column(String(255), nullable=True)
    environmentTag: Mapped[str | None] = mapped_column(String(255), nullable=True)
    instancePreference: Mapped[str] = mapped_column(
        String(255), nullable=False, default="default")
    resourceTags: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB), nullable=False, default=dict)
    resourceSpecInJSON: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB), nullable=False, default=dict)
