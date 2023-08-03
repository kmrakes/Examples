from typing import *

from pydantic import BaseModel, Field

from .MetaTypesEnum import MetaTypesEnum
from .StatusTypesEnum import StatusTypesEnum
from .TaskTypesEnum import TaskTypesEnum


class NewMeta(BaseModel):
    """
    NewMeta model
        General request model for X requests

    """

    code: str = Field(alias="code")

    parent: Optional[str] = Field(alias="parent", default=None)

    assigned: Optional[str] = Field(alias="assigned", default=None)

    status: Optional[Union[int, StatusTypesEnum]] = Field(alias="status", default=None)

    type: Optional[Union[int, MetaTypesEnum, TaskTypesEnum]] = Field(
        alias="type", default=None
    )

    metadata: Optional[Dict[str, Any]] = Field(alias="metadata", default=None)
