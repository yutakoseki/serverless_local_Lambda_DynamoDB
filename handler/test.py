import json
import boto3
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

if os.environ.get("IS_OFFLINE", "") == "true":
    dynamodb_client = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
else:
    dynamodb_client = boto3.client("dynamodb")

table_name = os.environ.get("DYNAMODB_TABLE_NAME", "")

def lambda_handler(event, context):
    # DynamoDBからのデータ取得
    try:
        response = dynamodb_client.scan(TableName=table_name)
        items = response.get("Items", [])

        # ページネーション処理
        while "LastEvaluatedKey" in response:
            response = dynamodb_client.scan(
                TableName=table_name, ExclusiveStartKey=response["LastEvaluatedKey"]
            )
            items.extend(response["Items"])

        # 結果をJSON形式で返す
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

# Lambdaハンドラのテスト実行
if __name__ == "__main__":
    # テスト用のダミーイベントとコンテキスト
    event = {}  # 必要に応じてモックイベントを定義
    context = None

    # lambda_handler関数を呼び出して結果を表示
    result = lambda_handler(event, context)
    print("Lambda Handlerの結果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
