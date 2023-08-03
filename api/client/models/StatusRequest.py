from typing import *

from pydantic import BaseModel, Field


class StatusRequest(BaseModel):
    """
    StatusRequest model
        Status request

    """

    status: int = Field(alias="status")
