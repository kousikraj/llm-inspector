#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: MIT-0

import json
import os

import boto3
import commons
from boto3.dynamodb.conditions import Attr

tableName = os.environ["llm_ddb"]
table = boto3.resource("dynamodb").Table(tableName)


def handler(event, context):
    # Get the object from the event and show its content type
    try:
        body = table.scan(FilterExpression=Attr("iTD").exists())
        items = body["Items"]
        payload = commons.get_response()
        payload["body"] = json.dumps(items, cls=commons.JSONEncoder)
        return payload
    except Exception as e:
        print("Error while getting list from the uploads table")
        print(e)
        return []
