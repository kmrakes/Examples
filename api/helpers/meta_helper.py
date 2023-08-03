# local
from ..client.services import Meta_service
from ..client.models import FilterMeta, NewMeta
from ..db_types import MetaTypes, TaskTypes
from ..utilities import sanitize_code
from ..classes.episode import Episode
from ..classes.sequence import Sequence
from ..classes.shot import Shot
from ..classes.task import Task


class MetaHelper:
    """ """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    # pylint: disable=too-many-arguments
    def _create_meta(
        self,
        code: str,
        metatype: int,
        parent=None,
        assigned: str = None,
        metadata: dict = None,
    ):
        """
        Convenience function to pass in our config
        """
        code = sanitize_code(code)
        if parent and not isinstance(parent, str):
            parent = parent.id
        data = NewMeta(
            code=code,
            parent=parent,
            assigned=assigned,
            type=metatype,
            metadata=metadata,
        )
        result = Meta_service.handler_meta_post(
            data, api_config_override=self.parent.config
        )
        return result

    def get_all_metas(self):
        """
        Get all meta objects
        """
        result = Meta_service.handler_meta_get(
            api_config_override=self.parent.config
        )
        return result

    def get_meta_by_id(self, oid):
        """ """
        result = Meta_service.handler_meta___id__get(
            oid, api_config_override=self.parent.config
        )
        return result

    # @ttl_cache(maxsize=100, ttl=120)
    def _get_meta_by_type(self, filter_type):
        """ """
        response = Meta_service.handler_meta_filter_post(
            FilterMeta(type=filter_type.id), api_config_override=self.parent.config
        )
        return response

    # @ttl_cache(maxsize=100, ttl=120)
    def _get_meta_by_code_type(self, code, filter_type):
        """ """
        response = Meta_service.handler_meta_filter_post(
            FilterMeta(code=code, type=filter_type.id),
            api_config_override=self.parent.config,
        )
        return response

    # @ttl_cache(maxsize=100, ttl=120)
    def get_meta_by_data(self, **kwargs):
        """
        gets all outMeta objects matching the provided kwargs
        """
        response = Meta_service.handler_meta_filter_post(
            FilterMeta(**kwargs), api_config_override=self.parent.config
        )

        return response

    def create_episode(self, code: str, metadata: dict = None):
        """ """
        response = self._create_meta(
            code, metatype=MetaTypes.EPISODE.id, metadata=metadata
        )
        episode = Episode(**response.dict(by_alias=True), parent=self.parent)
        return episode

    def create_sequence(self, code: str, parent=None, metadata: dict = None):
        """ """
        response = self._create_meta(
            code=code, parent=parent, metadata=metadata, metatype=MetaTypes.SEQUENCE.id
        )
        seq = Sequence(**response.dict(by_alias=True), parent=self.parent)
        return seq

    def create_shot(self, code: str, parent=None, metadata: dict = None):
        """ """
        response = self._create_meta(
            code=code, parent=parent, metadata=metadata, metatype=MetaTypes.SHOT.id
        )
        shot = Shot(**response.dict(by_alias=True), parent=self.parent)
        return shot

    # pylint: disable=too-many-arguments
    def create_task(
        self,
        code: str,
        parent=None,
        metadata: dict = None,
        assigned: str = "",
        tasktype=TaskTypes.COMP,
    ):
        """ """
        response = self._create_meta(
            code=code,
            parent=parent,
            assigned=assigned,
            metadata=metadata,
            metatype=tasktype.id,
        )
        task = Task(**response.dict(by_alias=True), parent=self.parent)
        return task

    def get_episodes(self):
        """ """
        response = self._get_meta_by_type(MetaTypes.EPISODE)
        return [Episode(**ep.dict(by_alias=True), parent=self.parent) for ep in response]

    def get_episode_by_id(self, oid: str):
        """ """
        response = self.get_meta_by_id(oid)
        episode = Episode(**response.dict(by_alias=True), parent=self.parent)
        return episode

    def get_episode_by_code(self, code: str):
        """ """
        response = self._get_meta_by_code_type(code, MetaTypes.EPISODE)
        if not response:
            return None
        return Episode(**response[0].dict(by_alias=True), parent=self.parent)

    def get_sequences(self):
        """ """
        response = self._get_meta_by_type(MetaTypes.SEQUENCE)
        return [
            Sequence(**seq.dict(by_alias=True), parent=self.parent) for seq in response
        ]

    def get_sequence_by_id(self, oid: str):
        """ """
        response = self.get_meta_by_id(oid)
        seq = Sequence(**response.dict(by_alias=True), parent=self.parent)
        return seq

    def get_sequence_by_code(self, code: str):
        """ """
        response = self._get_meta_by_code_type(code, MetaTypes.SEQUENCE)
        if not response:
            return None
        return Sequence(**response[0].dict(by_alias=True), parent=self.parent)

    def get_shot_by_id(self, oid: str):
        """ """
        response = self.get_meta_by_id(oid)
        shot = Shot(**response.dict(by_alias=True), parent=self.parent)
        return shot

    def get_shot_by_code(self, code: str):
        """ """
        response = self._get_meta_by_code_type(code, MetaTypes.SHOT)
        if not response:
            return None
        return Shot(**response[0].dict(by_alias=True), parent=self.parent)

    def get_task_by_id(self, oid: str):
        """ """
        response = self.get_meta_by_id(oid)
        task = Task(**response.dict(by_alias=True), parent=self.parent)
        return task

    def _filter_metas(self, items, meta_filters, meta_class):
        """ """
        filtered_items = []
        filters = [meta_filter.id for meta_filter in meta_filters]
        for item in items:
            if item.type.id in filters:
                filtered_items.append(
                    meta_class(**item.dict(by_alias=True), parent=self.parent)
                )
        return filtered_items

    def filter_tasks(self, items, task_filters):
        """ """
        return self._filter_metas(items, task_filters, Task)

    def filter_shots(self, items):
        """ """
        return self._filter_metas(items, [MetaTypes.SHOT], Shot)

    def filter_sequences(self, items):
        """ """
        return self._filter_metas(items, [MetaTypes.SEQUENCE], Sequence)
