import json
import boto3
import os

# DynamoDB Localへの接続
dynamodb_client = boto3.client("dynamodb", endpoint_url="http://localhost:8000")

table_name = os.environ.get("DYNAMODB_TABLE_NAME", "Movies-dev")

def lambda_handler(event, context):
    try:
        # DynamoDBからのデータ取得
        response = dynamodb_client.scan(TableName=table_name)
        items = response.get("Items", [])

        while "LastEvaluatedKey" in response:
            response = dynamodb_client.scan(
                TableName=table_name, ExclusiveStartKey=response["LastEvaluatedKey"]
            )
            items.extend(response["Items"])

        return {
            "statusCode": 200,
            "body": json.dumps(items),
        }
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }

if __name__ == "__main__":
    event = {}
    context = None
    result = lambda_handler(event, context)
    print("Lambda Handlerの結果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
