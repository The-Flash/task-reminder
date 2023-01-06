import json
import boto3
import os
import uuid

from typing import Union

SEND_REMINDER_FUNCTION_ARN = os.environ["SEND_REMINDER_FUNCTION"]
INVOKE_LAMBDA_SCHEDULER_ROLE_ARN = os.environ["INVOKE_LAMBDA_SCHEDULER_ROLE"]

scheduler_client = boto3.client("scheduler")


def lambda_handler(event, context):
    request_body = json.loads(event["body"])
    schedule_time = request_body["schedule_time"]
    title = request_body["title"]
    description = request_body["description"]

    scheduler_client.create_schedule(
        Name=str(uuid.uuid4()),
        FlexibleTimeWindow={
            "Mode": "OFF"
        },
        Target={
            "RoleArn": INVOKE_LAMBDA_SCHEDULER_ROLE_ARN,
            "Arn": SEND_REMINDER_FUNCTION_ARN,
            "Input": json.dumps({
                "Payload": {
                    "Title": title,
                    "Description": description
                }
            })
        },
        ScheduleExpression="at(%s)" % schedule_time
    )
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Successfully scheduled event"
        })
    }
