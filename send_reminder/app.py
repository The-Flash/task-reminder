# from services.response import HTTPResponse
from typing import Union

import boto3
import os
import json

TASK_QUEUE_ARN = os.environ["TASK_QUEUE"]
SENDER_EMAIL = os.environ["SENDER_EMAIL"]

ses_client = boto3.client("ses")
scheduler_client = boto3.client("scheduler")


def lambda_handler(event, context):
    try:
        records = event["Records"]
        for record in records:
            body = json.loads(record["body"])
            title = body["Title"]
            description = body["Description"]
            email = body["Email"]
            scheduleId = body["ScheduleId"]

            ses_client.send_email(
                Source=SENDER_EMAIL,
                Destination={
                    "ToAddresses": [email]
                },
                Message={
                    "Subject": {
                        "Data": "Reminder: %s" % title,
                    },
                    "Body": {
                        "Text": {
                            "Data": description
                        }
                    }
                }
            )
        scheduler_client.delete_schedule(
            Name=scheduleId
        )
        return True
    except Exception as e:
        print(e)
        return False
