from .base import Base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import String


class eventSourceDefnInstance(Base):
    __tablename__ = "eventSourceDefnInstance"

    type: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    EHName: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False)
    EHNameSpace: Mapped[str] = mapped_column(String(255), nullable=False)
    consumerGroup: Mapped[str] = mapped_column(String(255), nullable=False)
    consumerGroupStatus: Mapped[str] = mapped_column(String(255), nullable=False)
    resourceSpecInJSON: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB),
        nullable=False,
        default=dict
    )
