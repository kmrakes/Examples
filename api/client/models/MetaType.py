from typing import *

from pydantic import BaseModel, Field


class MetaType(BaseModel):
    """
    MetaType model

    """

    type: Optional[str] = Field(alias="type", default=None)

    id: int = Field(alias="id")

    value: str = Field(alias="value")
