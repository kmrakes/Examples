from typing import *

from pydantic import BaseModel, Field


class Metadata(BaseModel):
    """
    Metadata model
        Metadata request

    """

    field: str = Field(alias="field")

    value: str = Field(alias="value")
