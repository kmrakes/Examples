import json
from typing import *

import requests

from ..api_config import APIConfig, HTTPException
from ..models import *


def handler__endpoint_handler____id__note_get(
    _id: str,
    endpoint_handler: EndpointHandler,
    api_config_override: Optional[APIConfig] = None,
) -> List[OutNote]:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/{endpoint_handler}/{_id}/note"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }
    query_params: Dict[str, Any] = {}

    query_params = {
        key: value for (key, value) in query_params.items() if value is not None
    }

    response = requests.request(
        "get",
        f"{base_path}{path}",
        headers=headers,
        params=query_params,
        verify=api_config.verify,
    )
    if response.status_code != 200:
        raise HTTPException(
            response.status_code, f" failed with status code: {response.status_code}"
        )

    return [OutNote(**item) for item in response.json()]


def handler__endpoint_handler____id__note_post(
    _id: str,
    endpoint_handler: EndpointHandler,
    data: Note,
    api_config_override: Optional[APIConfig] = None,
) -> List[OutNote]:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/{endpoint_handler}/{_id}/note"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }
    query_params: Dict[str, Any] = {}

    query_params = {
        key: value for (key, value) in query_params.items() if value is not None
    }

    response = requests.request(
        "post",
        f"{base_path}{path}",
        headers=headers,
        params=query_params,
        verify=api_config.verify,
        json=data.dict(),
    )
    if response.status_code != 200:
        raise HTTPException(
            response.status_code, f" failed with status code: {response.status_code}"
        )

    return [OutNote(**item) for item in response.json()]


def handler__endpoint_handler____id__note__note_uid__seen__user__get(
    _id: str,
    note_uid: str,
    user: str,
    endpoint_handler: EndpointHandler,
    api_config_override: Optional[APIConfig] = None,
) -> Any:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/{endpoint_handler}/{_id}/note/{note_uid}/seen/{user}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }
    query_params: Dict[str, Any] = {}

    query_params = {
        key: value for (key, value) in query_params.items() if value is not None
    }

    response = requests.request(
        "get",
        f"{base_path}{path}",
        headers=headers,
        params=query_params,
        verify=api_config.verify,
    )
    if response.status_code != 200:
        raise HTTPException(
            response.status_code, f" failed with status code: {response.status_code}"
        )

    return response.json()


def handler__endpoint_handler____id__note__note_uid__delete(
    _id: str,
    note_uid: str,
    endpoint_handler: EndpointHandler,
    api_config_override: Optional[APIConfig] = None,
) -> Any:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/{endpoint_handler}/{_id}/note/{note_uid}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }
    query_params: Dict[str, Any] = {}

    query_params = {
        key: value for (key, value) in query_params.items() if value is not None
    }

    response = requests.request(
        "delete",
        f"{base_path}{path}",
        headers=headers,
        params=query_params,
        verify=api_config.verify,
    )
    if response.status_code != 200:
        raise HTTPException(
            response.status_code, f" failed with status code: {response.status_code}"
        )

    return response.json()
