import json
import boto3
import os
import uuid


SEND_MESSAGE_TO_QUEUE_ROLE_ARN = os.environ["SEND_MESSAGE_TO_QUEUE_ROLE"]
TASK_QUEUE_ARN = os.environ["TASK_QUEUE"]

scheduler_client = boto3.client("scheduler")


def lambda_handler(event, context):
    request_body = json.loads(event["body"])
    schedule_time = request_body["schedule_time"]
    title = request_body["title"]
    description = request_body["description"]
    email = request_body["email"]

    scheduleId = str(uuid.uuid4())
    scheduler_client.create_schedule(
        Name=scheduleId,
        FlexibleTimeWindow={
            "Mode": "OFF"
        },
        Target={
            "RoleArn": SEND_MESSAGE_TO_QUEUE_ROLE_ARN,
            "Arn": TASK_QUEUE_ARN,
            "Input": json.dumps({
                "Title": title,
                "Description": description,
                "Email": email,
                "ScheduleId": scheduleId
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
