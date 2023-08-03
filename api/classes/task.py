# std
import os

# local
from ..classes import MetaBase
from ..db_types import StateTypes, StatusTypes, MetaTypes
from .version import Version


class Task(MetaBase):
    """
    Helper class for a meta object representing a task

    Many of these attributes will be populated based on the
    metadata field from the database object.
    """

    @property
    def context(self) -> dict:
        """
        Returns a dict of the current context
        """
        return {**self.link.context, "task": self.code}

    def versions(self, version_types=None):
        """
        Grabs the children of a task, which should be versions
        """

        # version_ids_to_fetch = []
        versions = []
        if not version_types:
            # Need to loop through the following to consolidate
            # all versions
            version_types = [StateTypes.WORK, StateTypes.PUBLISH, StateTypes.DELIVERY]

        for version_type in version_types:
            if version_type == StateTypes.WORK:
                for ver in self.work:
                    versions.append(Version(**ver, luna=self.luna))
            if version_type == StateTypes.PUBLISH:
                for ver in self.publishes:
                    versions.append(Version(**ver, luna=self.luna))
            if version_type == StateTypes.DELIVERY:
                for ver in self.deliveries:
                    versions.append(Version(**ver, luna=self.luna))

        return versions

    def latest_version(self, version_types=None):
        """
        returns the latest version
        """

        versions = self.versions(version_types)

        if not versions:
            return None

        for version in sorted(versions, key=lambda k: k.version_number, reverse=True):
            return version

    # TODO: This is a bit of a hack, but it works for now. Need to find a better
    #  solution for the return types so they are consistent.
    # pylint: disable=inconsistent-return-statements
    @property
    def link(self):
        """ """
        # # TODO: If I keep these "OutMeta" objects, maybe call the parent "link"
        # # That way, we can use Task.parent (reads better as what the attribute is)
        # link = META_CACHE.get(self.parent.id)
        # if link:
        #     return link
        # Need to figure out what the parent type is
        parent_type = None
        for i in MetaTypes.options:
            # Need to match id's as self.parent.type returns a str
            if self.parent.type == i.id:
                parent_type = i
                break
        if not parent_type:
            return
        # Get the object from the database
        # TODO: Need to think about a more dynamic way of doing this
        if parent_type == MetaTypes.EPISODE:
            return self.parent.meta_helper.get_episode_by_id(self.parent.id)
        if parent_type == MetaTypes.SEQUENCE:
            return self.parent.meta_helper.get_sequence_by_id(self.parent.id)
        if parent_type == MetaTypes.SHOT:
            return self.parent.meta_helper.get_shot_by_id(self.parent.id)
        return self.parent

    # pylint: disable=too-many-arguments
    def create_version(
        self,
        code,
        version_number: int = 1,
        state=StateTypes.WORK,
        status=StatusTypes.WAITING_TO_START,
        source_version: str = None,
        author: str = "krakes",
    ):
        """
        Factory method for creating a Version and adding it to the
        global version cache
        """
        return self.parent.version_helper.create_version(
            code=code,
            parent=self.id,
            version_number=version_number,
            state=state,
            status=status,
            source_version=source_version,
            author=author,
        )

    @property
    def capsule(self):
        """
        Capsule location on disk
        Doing this, instead of making a call to the backend.
        These paths will always be formatted this way
        """
        return os.path.join("/show", self.id)
