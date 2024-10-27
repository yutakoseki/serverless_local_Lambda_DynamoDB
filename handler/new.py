# handler/new.py
import json
import boto3
import os

# 実行環境によって分岐
if os.environ.get("IS_OFFLINE", "") == "true":
    dynamodb_client = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
else:
    dynamodb_client = boto3.client("dynamodb")

table_name = os.environ.get("DYNAMODB_TABLE_NAME", "")

def lambda_handler(event, context):
    # DynamoDB からデータを取得
    response = dynamodb_client.scan(TableName=table_name)
    items = response.get("Items", [])
    
    # ページネーション
    while "LastEvaluatedKey" in response:
        response = dynamodb_client.scan(
            TableName=table_name, ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        items.extend(response["Items"])

    return {
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json; charset=utf-8"
    },
    "body": json.dumps({
        "message": "データ取得が完了しました。",
        "data": items
    }, ensure_ascii=False)
}