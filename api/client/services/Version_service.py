import json
from typing import *

import requests

from ..api_config import APIConfig, HTTPException
from ..models import *


def handler_version___id__state_post(
    _id: str, data: StateRequest, api_config_override: Optional[APIConfig] = None
) -> OutVersion:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/version/{_id}/state"
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

    return (
        OutVersion(**response.json()) if response.json() is not None else OutVersion()
    )


def handler_version_filter_post(
    data: FilterVersion, api_config_override: Optional[APIConfig] = None
) -> List[OutVersion]:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/version/filter"
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

    return [OutVersion(**item) for item in response.json()]


def handler_version_get(
    api_config_override: Optional[APIConfig] = None,
) -> List[OutVersion]:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/version"
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

    return [OutVersion(**item) for item in response.json()]


def handler_version_post(
    data: NewVersion, api_config_override: Optional[APIConfig] = None
) -> OutVersion:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/version"
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

    return (
        OutVersion(**response.json()) if response.json() is not None else OutVersion()
    )


def handler_version___id__get(
    _id: str, api_config_override: Optional[APIConfig] = None
) -> OutVersion:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/version/{_id}"
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

    return (
        OutVersion(**response.json()) if response.json() is not None else OutVersion()
    )


def handler_version___id__put(
    _id: str, data: UpdateVersion, api_config_override: Optional[APIConfig] = None
) -> OutVersion:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/version/{_id}"
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
        "put",
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

    return (
        OutVersion(**response.json()) if response.json() is not None else OutVersion()
    )


def handler_version___id__delete(
    _id: str, api_config_override: Optional[APIConfig] = None
) -> Any:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/version/{_id}"
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


def handler_version_batch_post(
    data: List[NewVersion], api_config_override: Optional[APIConfig] = None
) -> List[OutVersion]:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/version/batch"
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
        json=[i.dict() for i in data],
    )
    if response.status_code != 200:
        raise HTTPException(
            response.status_code, f" failed with status code: {response.status_code}"
        )

    return [OutVersion(**item) for item in response.json()]


def handler_version___id__x_file_get(
    _id: str, api_config_override: Optional[APIConfig] = None
) -> List[OutXFile]:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/version/{_id}/x-file"
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

    return [OutXFile(**item) for item in response.json()]


def handler_version___id__x_file_post(
    _id: str, data: XFile, api_config_override: Optional[APIConfig] = None
) -> OutVersion:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/version/{_id}/x-file"
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

    return (
        OutVersion(**response.json()) if response.json() is not None else OutVersion()
    )
