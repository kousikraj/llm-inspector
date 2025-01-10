import decimal
import math
import datetime
import boto3
import json
from decimal import Decimal
from botocore.exceptions import ClientError
from core.api.commons import constants
from core.api.commons.request_payload import RequestPayload

table = boto3.resource("dynamodb").Table(constants.DDB_NAME)
s3_client = boto3.client("s3")
bucket_name = constants.S3_BUCKET_NAME
bucket_prefix = "images/"


class DecimalToFloatEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return math.floor(float(o))
        return super().default(o)


def get_image_without_tmp_path(image_path: str):
    return image_path.replace(constants.LOCAL_TEMP_FOLDER_PATH, "")


def get_request_id(req_id: str, image: str):
    image = get_image_without_tmp_path(image)
    return req_id + "|" + image


def get_s3_bucket_and_prefix():
    return bucket_name, bucket_prefix


def save_images_and_payload(
    generated_response, generated_images: [], request_payload_object: RequestPayload
):
    for image in generated_images:
        upload_to_s3(image)
        p = request_payload_object.toJSON()
        r = generated_response
        ddb_item = {
            "mId": request_payload_object.model_id,
            "rId": get_request_id(request_payload_object.req_id, image),
            "p": p,
            "r": r,
        }
        save_to_ddb(ddb_item)


def upload_to_s3(local_file_path):
    try:
        s3_client.upload_file(
            local_file_path,
            bucket_name,
            f"{bucket_prefix}{get_image_without_tmp_path(local_file_path)}",
        )
    except ClientError as e:
        print(f"Error saving response: {e}")


def save_to_ddb(ddb_item):
    print("Utility: Saving Prompt to DDB")
    try:
        now = datetime.datetime.now()
        ddb_item["gTD"] = now.isoformat()
        response = table.put_item(
            Item=json.loads(json.dumps(ddb_item), parse_float=Decimal)
        )
        print(response)
        print(f"JSON data saved successfully to DynamoDB table: {constants.DDB_NAME}")
    except Exception as e:
        print(f"Error saving JSON data to DynamoDB: {e}")


def update_to_ddb(model_id, req_id, image, inspector_response):
    print("Utility: Saving Prompt to DDB")
    try:
        inspector_response_text = inspector_response["content"][0]["text"]
        del inspector_response["content"]
        now = datetime.datetime.now()
        response = table.update_item(
            Key={
                "mId": model_id,
                "rId": get_request_id(req_id, image),
            },
            UpdateExpression="SET iRes = :iRes, iMeta = :iMeta, iTD = :iTD",
            ExpressionAttributeValues={
                ":iRes": json.loads(inspector_response_text),
                ":iMeta": inspector_response,
                ":iTD": now.isoformat(),
            },
            ReturnValues="UPDATED_NEW",
        )
        print(response)
        print(f"JSON data saved successfully to DynamoDB table: {constants.DDB_NAME}")
    except Exception as e:
        print(f"Error saving JSON data to DynamoDB: {e}")


def read_file_to_string(file_path):
    """
    Reads the contents of a text file and returns it as a string.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str: The contents of the text file as a string.
    """
    try:
        with open(file_path, "r") as file:
            file_contents = file.read()
        return file_contents
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except IOError:
        print(f"Error: Unable to read file at {file_path}")
        return None
