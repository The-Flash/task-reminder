# from services.response import HTTPResponse
from typing import Union

import boto3
import os
import json

TASK_REMINDER_TOPIC_ARN = os.environ["TASK_REMINDER_TOPIC"]
TASK_QUEUE_ARN = os.environ["TASK_QUEUE"]

sns_client = boto3.client("sqs")


def lambda_handler(event, context):
    print("Passed Event", event)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Lambda has been called",
        })
    }
