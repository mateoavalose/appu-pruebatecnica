import boto3
from django.conf import settings

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_DEFAULT_REGION
)

table = dynamodb.Table(settings.DYNAMODB_TABLE_NAME)

def create_document(data:dict) -> dict:
    table.put_item(Item=data)
    return data

def get_document_by_id(document_id: str) -> dict:
    response = table.get_item(Key={'id': document_id})
    return response.get('Item', {})

def get_documents_by_name(name: str) -> list:
    response = table.query(
        IndexName='file_name-index',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('file_name').eq(name)
    )
    return response.get('Items', [])

def update_document(document_id: str, updates: dict) -> dict:
    update_expression = "SET " + ", ".join(f"{k}=:{k}" for k in updates.keys())
    expression_values = {f":{k}": v for k, v in updates.items()}
    table.update_item(
        Key={'id': document_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values
    )
    return get_document_by_id(document_id)

def delete_document(document_id: str) -> None:
    table.delete_item(Key={'id': document_id})
    return None