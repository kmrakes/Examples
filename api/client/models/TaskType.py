from typing import *

from pydantic import BaseModel, Field


class TaskType(BaseModel):
    """
    TaskType model

    """

    type: Optional[str] = Field(alias="type", default=None)

    id: int = Field(alias="id")

    value: str = Field(alias="value")
