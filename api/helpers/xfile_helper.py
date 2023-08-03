# local
from ..client.services import XFile_service
from ..client.models import XFile
from ..db_types import FileTypes
from ..utilities import sanitize_code
from ..classes import x_file


class FileHelper:
    """ """

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    # pylint: disable=too-many-arguments
    def create_file(
        self,
        oid: str,
        code: str,
        path: str,
        metadata: dict,
        filetype=FileTypes.FRAMES,
    ):
        """
        oid: Object id of the version to attach the file to
        data: Data to be used in the creation of the XFile
        """

        if not isinstance(metadata, dict):
            # Data must be a dictionary of data
            return None
        code = sanitize_code(code)

        x_model = XFile(
            file_type=filetype, code=code, path=path, metadata=metadata
        )
        response = XFile_service.handler_version___id__x_file_post(
            _id=oid, data=x_model, api_config_override=self.parent.config
        )

        # Return a x file object
        return response

    def get_version_xfiles(self, oid: str):
        """ """
        response = XFile_service.handler_version___id__x_file_get(oid)

        return [
            x_file.XF(**xfile.dict(by_alias=True)) for xfile in response
        ]
