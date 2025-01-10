#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: MIT-0

import json
import logging

import boto3
import commons
import os
from urllib.parse import unquote

s3_client = boto3.client("s3")

tableName = os.environ["llm_ddb"]
table = boto3.resource("dynamodb").Table(tableName)


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except Exception as e:
        print(e)
        print("Error while getting list from the uploads table")
        return None

    # The response contains the presigned URL
    return response


def handler(event, context):
    key = event["path"]
    payload = commons.get_response()
    try:
        keys = key.split("_")
        rId = unquote(keys[1])
        mId = keys[0].replace("/details/", "")
        object_from_table = table.get_item(
            Key={
                "mId": mId,
                "rId": rId,
            },
            ConsistentRead=True,
        )
        if "Item" in object_from_table.keys():
            ddb_item = object_from_table["Item"]
            s3_key = "images/" + rId.split("|")[1]
            s3_signed_url = create_presigned_url(os.environ["llm_s3"], s3_key)
            payload["body"] = json.dumps(
                {
                    "item": ddb_item,
                    "presignedUrl": s3_signed_url,
                },
                cls=commons.JSONEncoder,
            )
            print(payload)
        return payload
    except Exception as e:
        print("Error while getting item from the audit table")
        print(e)
        return []
