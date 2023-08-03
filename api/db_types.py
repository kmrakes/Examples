"""
Types output models
"""
# std
from enum import Enum
from typing import Union
from logging import getLogger

# 3rd
from pydantic import BaseModel


LOGGER = getLogger("uvicorn")


#########
# Bases #
#########


class TypeCollection(type):
    """
    Provides a metaclass that injects the options property into the classes
    """

    @property
    def options(cls):
        """
        Returns a list of all the options in the class
        """
        return [cls.__dict__[i] for i in cls.__dict__ if i.isupper()]


class SelfDocEnum(int, Enum):
    """
    Adds in functionality that provides a docstring for the enum that is compatible
    with FastAPI's Swagger UI.
    """

    @classmethod
    def generate_doc(cls):
        """
        Generates a docstring for the enum that is compatible with FastAPI's Swagger UI
        """
        docs = "Options:\n"
        for option in cls:
            docs += f"  - {option.name}: {option.value}\n"
        cls.__doc__ = docs


class BaseCollection(metaclass=TypeCollection):
    """
    Defines how base collections should behave in the eyes of Luna types
    """

    @classmethod
    def to_enum(cls):
        """
        Returns a SelfDocEnum of the class in question. It is compatible with FastAPI's Swagger UI
        """
        # from pprint import pprint
        values = [(i.value.upper(), int(i.id)) for i in cls.options]
        enum = SelfDocEnum(f"{cls.__name__}Enum", values)
        enum.generate_doc()
        return enum


#########
# Types #
#########


class MetaType(BaseModel):
    type: str = "META"
    id: int
    value: str


class TaskType(BaseModel):
    type: str = "TASK"
    id: int
    value: str


class StateType(BaseModel):
    type: str = "STATE"
    id: int
    value: str
    color: str


class FileType(BaseModel):
    type: str = "FILE"
    id: int
    value: str


class StatusType(BaseModel):
    type: str = "STATUS"
    id: int
    value: str
    color: str


class NoteType(BaseModel):
    type: str = "NOTE"
    id: int
    value: str
    color: str


class ProjectType(BaseModel):
    type: str = "PROJECT"
    id: int
    value: str


###############
# Collections #
###############


class ProjectTypes(BaseCollection):
    EPISODIC = ProjectType(id=9010, value="Episodic")
    FEATURE = ProjectType(id=9020, value="Feature")
    COMMERCIAL = ProjectType(id=9030, value="Commercial")


class MetaTypes(BaseCollection):
    EPISODE = MetaType(id=1010, value="Episode")
    SEQUENCE = MetaType(id=1020, value="Sequence")
    SHOT = MetaType(id=1030, value="Shot")


class TaskTypes(BaseCollection):
    COMP = TaskType(id=1040, value="Comp")
    ROTO = TaskType(id=1050, value="Roto")
    PAINT = TaskType(id=1060, value="Paint")
    INGEST = TaskType(id=1070, value="Ingest")


class StateTypes(BaseCollection):
    WORK = StateType(id=2010, value="Work", color="FFF633")
    PUBLISH = StateType(id=2020, value="Publish", color="33F0FF")
    DELIVERY = StateType(id=2030, value="Delivery", color="5EFF33")


class FileTypes(BaseCollection):
    FRAMES = FileType(id=3010, value="Frames")
    REFERENCE = FileType(id=3020, value="Ref")
    LUT = FileType(id=3030, value="Lut")
    SCENE = FileType(id=3040, value="Scene")
    TEXTURE = FileType(id=3050, value="Texture")


class StatusTypes(BaseCollection):
    APPROVED = StatusType(id=5010, value="APPROVED", color="5EFF33")
    REJECTED = StatusType(id=5020, value="REJECTED", color="FF3333")
    WORK_IN_PROGRESS = StatusType(id=5030, value="WORK_IN_PROGRESS", color="FFF633")
    PENDING_INTERNAL_REVIEW = StatusType(
        id=5040, value="PENDING_INTERNAL_REVIEW", color="33F0FF"
    )
    PENDING_CLIENT_REVIEW = StatusType(
        id=5050, value="PENDING_CLIENT_REVIEW", color="335EFF"
    )
    WAITING_TO_START = StatusType(id=5060, value="WAITING_TO_START", color="CE33FF")
    READY_TO_START = StatusType(id=5070, value="READY_TO_START", color="FF33BE")


class NoteTypes(BaseCollection):
    CLIENT = NoteType(id=4010, value="CLIENT", color="FF3333")
    INTERNAL = NoteType(id=4020, value="INTERNAL", color="33FFF6")
    CBB = NoteType(id=4030, value="CBB", color="E0FF33")


# TODO: This is a hacky way to do this. I need to find a better way to do this.
#########
# Enums #
#########

ProjectEnum = ProjectTypes.to_enum()
MetaEnum = MetaTypes.to_enum()
TaskEnum = TaskTypes.to_enum()
StateEnum = StateTypes.to_enum()
FileEnum = FileTypes.to_enum()
StatusEnum = StatusTypes.to_enum()
NoteEnum = NoteTypes.to_enum()

##############
# Type Hints #
##############

# pylint: disable=invalid-name
TYPES = Union[
    MetaType, TaskType, NoteType, StateType, FileType, StatusType, ProjectType
]
DEFAULTS = [
    MetaTypes,
    TaskTypes,
    StateTypes,
    FileTypes,
    StatusTypes,
    NoteTypes,
    ProjectTypes,
]
METAS = Union[MetaType, TaskType]
