import decimal
import json
from decimal import Decimal


def convert_dynamodb_item_to_json(item):
    """Converts a DynamoDB item to JSON.

    Args:
      item: A DynamoDB item.

    Returns:
      A JSON string.
    """
    json_item = {}
    for key, value in item.items():
        if isinstance(value, dict):
            json_item[key] = convert_dynamodb_item_to_json(value)
        elif isinstance(value, list):
            json_item[key] = [convert_dynamodb_item_to_json(v) for v in value]
        elif isinstance(value, Decimal):
            return float(value)
        else:
            json_item[key] = value

    return json.dumps(json_item)


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super().default(o)


def get_response():
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
    }


def get_err_response():
    return {
        "statusCode": 500,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
    }
