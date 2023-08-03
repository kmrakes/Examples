from typing import *

from pydantic import BaseModel, Field


class StatusType(BaseModel):
    """
    StatusType model

    """

    type: Optional[str] = Field(alias="type", default=None)

    id: int = Field(alias="id")

    value: str = Field(alias="value")

    color: str = Field(alias="color")
