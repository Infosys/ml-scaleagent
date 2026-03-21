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
