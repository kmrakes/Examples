# std
from typing import Any, List

# 3rd
from pydantic import validator

# local
from jfx_luna.client.models import OutMeta
from ..db_types import TaskTypes


class MetaBase(OutMeta):
    """
    Base object for all metas
    """

    parent: Any

    class Config:
        """ """

        # exclude = ['children']
        arbitrary_types_allowed = True

    def dict(self, *args, exclude=None, **kwargs):
        """
        Hack for dealing with pydantic
        """
        if exclude:
            exclude = exclude.add("children")
        else:
            exclude = {"children"}

        return super().dict(exclude=exclude, *args, **kwargs)

    @validator("children")
    # pylint: disable=no-self-argument,import-outside-toplevel,unused-argument,unused-argument
    def hydrate_children(cls, children, values, **kwargs) -> List:
        """
        TODO: fill me in
        """
        from ..main import X

        return [X().meta_helper.get_meta_by_id(child.id) for child in children]

    @property
    def context(self):
        """ """
        raise NotImplementedError

    def is_task(self) -> bool:
        """
        Hmm
        """
        if not self.type:
            return False

        return self.type.value.upper() in TaskTypes.__dict__
