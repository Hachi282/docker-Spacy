import spacy
import json
import logging
import boto3
from boto3.dynamodb.types import TypeSerializer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

nlp = spacy.load("zh_core_web_sm")

# Create  DynamoDB resource
dynamodb = boto3.resource("dynamodb")
table_name = "line"
table = dynamodb.Table(table_name)


def handler(event, context):
    # Define function to update user message in DynamoDB
    def update_message(m_id, text):
        table.update_item(
            Key={"user_id": m_id},
            UpdateExpression="set unpack_message = :msg",
            ExpressionAttributeValues={":msg": text},
            ReturnValues="UPDATED_NEW",
        )
        logger.info(f"completed change")

    # payload = json.loads(event["body"])
    # m_id = payload.get("m_id")
    # messageText = payload.get("messageText")
    # reply_token = payload.get("reply_token")
    m_id = event["m_id"]
    messageText = event["messageText"]
    logger.info(
        f"Received m_id: {m_id}, messageText: {messageText}"
    )

    doc = nlp(messageText)
    result = [(w.text, w.pos_) for w in doc]
    serializer = TypeSerializer()
    new_result = [serializer.serialize(value) for value in result]

    update_message(m_id, new_result)

    response = {
        "statusCode": 200,
        "body": json.dumps("Successfully processed Spacy Lambda."),
    }

    return response
