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
