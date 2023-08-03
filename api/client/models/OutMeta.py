from typing import *

from pydantic import BaseModel, Field

from .FileType import FileType
from .MetaType import MetaType
from .NoteType import NoteType
from .OutNote import OutNote
from .ProjectType import ProjectType
from .RelatedOutMeta import RelatedOutMeta
from .StateType import StateType
from .StatusType import StatusType
from .TaskType import TaskType


class OutMeta(BaseModel):
    """
        OutMeta model
            Handles the _id issue with mongodb. This uses the above PyObjectId
    class to handle it.

    """

    id: Optional[str] = Field(alias="_id", default=None)

    code: str = Field(alias="code")

    type: Union[
        MetaType, TaskType, NoteType, StateType, FileType, StatusType, ProjectType
    ] = Field(alias="type")

    parent: Optional[RelatedOutMeta] = Field(alias="parent", default=None)

    assigned: Optional[str] = Field(alias="assigned", default=None)

    metadata: Optional[Dict[str, Any]] = Field(alias="metadata", default=None)

    status: Optional[StatusType] = Field(alias="status", default=None)

    notes: Optional[List[Optional[OutNote]]] = Field(alias="notes", default=None)

    created: str = Field(alias="created")

    modified: Optional[str] = Field(alias="modified", default=None)

    children: Optional[List[Optional[RelatedOutMeta]]] = Field(
        alias="children", default=None
    )

    deliveries: Optional[List[Any]] = Field(alias="deliveries", default=None)

    publishes: Optional[List[Any]] = Field(alias="publishes", default=None)

    work: Optional[List[Any]] = Field(alias="work", default=None)
