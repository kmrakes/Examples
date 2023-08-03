# std
import os
import requests

# 3rd
from jfx_utils.logger.logger import get_logger

# local
from .client import api_config
from .db_types import TaskTypes, FileTypes
from .helpers.project_helper import ProjectHelper
from .helpers.meta_helper import MetaHelper
from .helpers.xfile_helper import FileHelper
from .helpers.version_helper import VersionHelper


LOGGER = get_logger()


class X:
    """
    This class stores all the functions to interact with the database.
    """

    def __init__(self):
        """ """
        super().__init__()
        self.config = api_config.APIConfig(
            base_path=f"http://{os.environ.get('X', 'x')}:8000"
        )
        self._project_helper = None
        self._meta_helper = None
        self._file_helper = None
        self._version_helper = None

    @property
    def project_helper(self):
        """ """
        if not self._project_helper:
            self._project_helper = ProjectHelper(self)
        return self._project_helper

    @property
    def meta_helper(self):
        """ """
        if not self._meta_helper:
            self._meta_helper = MetaHelper(self)
        return self._meta_helper

    @property
    def xfile_helper(self):
        """ """
        if not self._file_helper:
            self._ile_helper = FileHelper(self)
        return self._file_helper

    @property
    def version_helper(self):
        """ """
        if not self._version_helper:
            self._version_helper = VersionHelper(self)
        return self._version_helper

    def create_episode(self, code, metadata: dict = None):
        """ """
        return self.meta_helper.create_episode(code, metadata)

    def create_sequence(self, code, parent=None, metadata=None):
        """ """
        return self.meta_helper.create_sequence(
            code=code, parent=parent, metadata=metadata
        )

    def create_shot(self, code, parent=None, metadata=None):
        """ """
        return self.meta_helper.create_shot(code=code, parent=parent, metadata=metadata)

    # pylint: disable=too-many-arguments
    def create_task(
        self, code, parent=None, assigned=None, metadata=None, tasktype=TaskTypes.COMP
    ):
        """ """
        return self.meta_helper.create_task(
            code=code,
            parent=parent,
            metadata=metadata,
            assigned=assigned,
            tasktype=tasktype,
        )

    # pylint: disable=too-many-arguments
    def create_file(
        self,
        oid: str,
        code: str,
        path: str,
        metadata: dict,
        filetype=FileTypes.FRAMES,
    ):
        """ """
        # pylint: disable=too-many-arguments
        return self.file_helper.create_file(
            oid, code, path, metadata, filetype.id
        )

    def get_project(self):
        """ """
        return self.project_helper.get_project()

    def get_episodes(self):
        """ """
        return self.meta_helper.get_episodes()

    def get_sequences(self):
        """ """
        return self.meta_helper.get_sequences()

    def get_episode(self, code: str = None, oid: str = None):
        """ """
        if not code and not oid:
            # pylint: disable=broad-exception-raised
            raise Exception("Please provide a code / oid")
        if oid:
            return self.meta_helper.get_episode_by_id(oid)
        return self.meta_helper.get_episode_by_code(code)

    def get_sequence(self, code: str = None, oid: str = None):
        """ """
        if not code and not oid:
            # pylint: disable=broad-exception-raised
            raise Exception("Please provide a code / oid")
        if oid:
            return self.meta_helper.get_sequence_by_id(oid)
        return self.meta_helper.get_sequence_by_code(code)

    def get_shot(self, code: str = None, oid: str = None):
        """ """
        if not code and not oid:
            # pylint: disable=broad-exception-raised
            raise Exception("Please provide a code / oid")
        if oid:
            return self.meta_helper.get_shot_by_id(oid)
        return self.meta_helper.get_shot_by_code(code)

    def get_task_by_id(self, oid: str):
        """ """
        return self.meta_helper.get_task_by_id(oid)

    @staticmethod
    # pylint: disable=invalid-name,redefined-builtin
    def get_web_thumbnail(type: str, id: str):
        """
        returns our webb url for requested thumbnail
        """
        try:
            response = requests.get(
                f"http://web:8000/web/thumb/{type}/{id}", timeout=5
            )
        # pylint: disable=bare-except
        except:
            LOGGER.warning(f"No thumbnail for {type}/{id}...safely skipping")
            return None

        if response.status_code != 200:
            return None

        return response
