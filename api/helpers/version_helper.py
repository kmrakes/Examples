# local
from ..client.services import Version_service
from ..client.models import NewVersion, FilterVersion, StateRequest, UpdateVersion
from ..db_types import StatusTypes, StateTypes, StateType, StatusType
from ..classes.version import Version


class VersionHelper:
    """ """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    # pylint: disable=too-many-arguments
    def create_version(
        self,
        code: str,
        parent: str = None,
        version_number: int = 1,
        state: StateType = StateTypes.WORK,
        status: StatusType = StatusTypes.WAITING_TO_START,
        source_version: str = None,
        author: str = "x",
        metadata: dict = None,
    ):
        """ """
        new_version = NewVersion(
            code=code,
            parent=parent,
            version_number=version_number,
            state=state.id,
            status=status.id,
            source_version=source_version,
            author=author,
            metadata={} if not metadata else metadata,
        )
        response = Version_service.handler_version_post(
            data=new_version, api_config_override=self.parent.config
        )
        return Version(**response.dict(by_alias=True), parent=self.parent)

    # @ttl_cache(maxsize=100, ttl=120)
    def get_task_versions_by_state(self, task_id, version_state: StateType):
        """ """

        filter_data = FilterVersion(parent=task_id, state=version_state.id)
        response = Version_service.handler_version_filter_post(
            filter_data, api_config_override=self.parent.config
        )
        return [Version(**v.dict(by_alias=True), parent=self.parent) for v in response]

    # @ttl_cache(maxsize=100, ttl=120)
    def get_task_versions_by_status(self, version_status: StatusType):
        """ """
        raise NotImplementedError("Under Development")

    # @ttl_cache(maxsize=100, ttl=120)
    def get_version_by_id(self, oid: str):
        """ """
        response = Version_service.handler_version___id__get(
            oid, api_config_override=self.parent.config
        )
        return Version(**response.dict(by_alias=True), parent=self.parent)

    def update_version_state(self, _id: str, state: StateType = StateTypes.PUBLISH):
        """ """
        response = Version_service.handler_version___id__state_post(
            _id, StateRequest(state=state.id), api_config_override=self.parent.config
        )
        return Version(**response.dict(by_alias=True), parent=self.parent)

    def update_version_status(
        self, _id: str, status: StatusTypes = StatusTypes.WAITING_TO_START
    ):
        """ """

        response = Version_service.handler_version___id__put(
            _id, UpdateVersion(status=status.id), api_config_override=self.parent.config
        )
        return Version(**response.dict(by_alias=True), parent=self.parent)
