import json

from typing import Union


def HTTPResponse(
    *,
    statusCode=200,
    body: Union[dict, None] = None,
    headers: dict = {}
):
    return {
        "statusCode": statusCode,
        "body": json.dumps(body),
        "headers": json.dumps(headers)
    }
