from typing import *

from pydantic import BaseModel, Field

from .FileTypesEnum import FileTypesEnum


class XFile(BaseModel):
    """
    XFile model

    """

    file_type: Union[int, FileTypesEnum] = Field(alias="file_type")

    code: str = Field(alias="code")

    path: str = Field(alias="path")

    metadata: Optional[Dict[str, Any]] = Field(alias="metadata", default=None)
