import json
from typing import *

import requests

from ..api_config import APIConfig, HTTPException
from ..models import *


def handler__endpoint_handler____id__status_post(
    _id: str,
    endpoint_handler: EndpointHandler,
    data: StatusRequest,
    api_config_override: Optional[APIConfig] = None,
) -> Union[OutMeta, OutVersion]:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/{endpoint_handler}/{_id}/status"
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
        Union[OutMeta, OutVersion](**response.json())
        if response.json() is not None
        else Union[OutMeta, OutVersion]()
    )
