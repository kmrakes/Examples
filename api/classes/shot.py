# 3rd party
from x_utils.logger.logger import get_logger

# local imports
from ..classes import MetaBase
from ..db_types import TaskTypes, TaskType
from ..utilities import sanitize_code
from .task import Task

LOGGER = get_logger()


class Shot(MetaBase):
    """
    Helper class for a meta object representing a shot

    Many of these attributes will be populated based on the
    metadata field from the database object.
    """

    @property
    def context(self) -> dict:
        """
        Returns a dict of the current context
        """
        return {**self.sequence.context, "shot": self.code}

    @property
    def sequence(self):
        """ """
        return self.parent.meta_helper.get_sequence_by_id(self.parent.id)

    @property
    def length(self):
        """ """
        return self.metadata.get("shot_length", 0)

    @property
    def first_frame(self):
        """ """
        return self.metadata.get("first_frame", 1001)

    @property
    def last_frame(self):
        """ """
        return self.first_frame + self.length

    @property
    def cut_in(self):
        """ """
        return self.metadata.get("cut_in", 0)

    @property
    def cut_out(self):
        """ """
        return self.metadata.get("cut_out", 0)

    @property
    def head_handles(self):
        """ """
        return self.metadata.get("head_handles", 8)

    @property
    def tail_handles(self):
        """ """
        return self.metadata.get("tail_handles", 8)

    @property
    def aspect_ratio(self):
        """ """
        # NOTE: Generally set to the show not a shot, can possibly be removed
        return self.metadata.get("aspect_ratio", "16:9")

    @property
    def timecode(self):
        """ """
        # TODO: use a timecode module
        # NOTE: Generally set to the show not a shot, can possibly be removed
        return self.metadata.get("timecode", "00:00:00:00")

    @property
    def width(self):
        """ """
        # NOTE: Generally set to the show not a shot, can possibly be removed
        return self.metadata.get("width", 1920)

    @property
    def height(self):
        """ """
        # NOTE: Generally set to the show not a shot, can possibly be removed
        return self.metadata.get("height", 1080)

    @property
    def tasks(self):
        """ """
        tasks = self.parent.meta_helper.filter_tasks(self.children, TaskTypes.options)
        return tasks

    def get_tasks(self, **kwargs) -> list:
        """
        get tasks matching data provided. Converts the outMeta objects to our class objects
        """
        metas = []
        parent = kwargs.get("parent")
        if parent and parent != self.id:
            LOGGER.warning("Parent id provided does not match shot id...overriding")

        kwargs["parent"] = self.id

        tasks = self.parent.meta_helper.get_meta_by_data(**kwargs)

        # convert the outMeta objects to our task class
        for task in tasks:
            metas.append(Task(**task.dict(by_alias=True), luna=self.luna))

        return metas

    def get_task(self, **kwargs):
        """
        get first task that matches the provided data
        """
        tasks = self.get_tasks(**kwargs)
        if tasks:
            return tasks[0]

        return None

    def create_task(self, code: str, tasktype: TaskType = TaskTypes.COMP):
        """
        Helper function for creating a task meta linked to this shot.
        code (str): Name of the task
        tasktype (str): Id for the task type, defaults to COMP
        """
        code = sanitize_code(code)
        task = self.parent.create_task(code=code, parent=self.id, tasktype=tasktype)
        self.children.append(task)  # TODO: Cast this to a RelatedMetaObject
        return task
