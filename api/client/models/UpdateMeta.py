from typing import *

from pydantic import BaseModel, Field

from .StatusTypesEnum import StatusTypesEnum


class UpdateMeta(BaseModel):
    """
    UpdateMeta model
        General request model for X requests

    """

    code: Optional[str] = Field(alias="code", default=None)

    parent: Optional[str] = Field(alias="parent", default=None)

    assigned: Optional[str] = Field(alias="assigned", default=None)

    status: Optional[Union[int, StatusTypesEnum]] = Field(alias="status", default=None)

    metadata: Optional[Dict[str, Any]] = Field(alias="metadata", default=None)
