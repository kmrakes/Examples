# local
from ..client.services import Project_service
from ..classes.project import Project


class ProjectHelper:
    """ """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    def get_project(self):
        """
        Returns the project object
        """

        response = Project_service.handler_project_get(
            api_config_override=self.parent.config
        )
        project = Project(**response.dict(by_alias=True))
        return project
