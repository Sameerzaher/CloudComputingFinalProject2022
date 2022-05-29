import json
import string
from datetime import datetime
from random import choices
import uuid
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    print(event)
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("url_shortener")

    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    
    if "routeKey" in event and event["routeKey"] == "POST /":
        data = json.loads(event["body"])
        url_long = data["url_long"]
        url_short = generate_short_id(url_long)
        table.put_item(
                Item={
                    "url_short": url_short,
                    "url_long": url_long,
                    "created_date": date_time,
                    "id": str(uuid.uuid4()),
                }
            )
        response = table.get_item(
            Key={
                'url_short': url_short
            }
        )
        return response['Item']
    
    elif "routeKey" in event and event["routeKey"] == "GET /":
        response = table.query(KeyConditionExpression=Key('url_short').eq(event["queryStringParameters"]["url_short"]))
        return response['Items'][0]
    if event['type'] == 'POST':
        data = event
        url_long = data["url_long"]
        url_short = generate_short_id(url_long)
        table.put_item(
                Item={
                    "url_short": url_short,
                    "url_long": url_long,
                    "created_date": date_time,
                    "id": str(uuid.uuid4()),
                }
            )
        response = table.get_item(
            Key={
                'url_short': url_short
            }
        )
        return response['Item']
    elif event['type'] == 'GET' :
        response = table.query(KeyConditionExpression=Key('url_short').eq(event["url_short"]))
        return response['Items'][0]


def generate_short_id(url):
    """generate random keys for short ulrs"""
    base_url = "d2nxqj63w4d6io.cloudfront.net/"
    url_short = "".join(choices(string.ascii_letters + string.digits, k=6))
    return base_url + url_short