from typing import *

from pydantic import BaseModel, Field


class OutMetaType(BaseModel):
    """
        OutMetaType model
            Handles the _id issue with mongodb. This uses the above PyObjectId
    class to handle it.

    """

    id: Optional[str] = Field(alias="_id", default=None)

    type: Optional[str] = Field(alias="type", default=None)

    value: str = Field(alias="value")
