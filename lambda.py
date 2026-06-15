import json
import boto3
from datetime import datetime

# S3のObject Createdイベントをトリガーとして実行
# アップロードされたファイル情報をDynamoDBへ保存する

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = "PortfolioFileMetadata"

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    try:
        for record in event["Records"]:

            # S3イベント情報取得
            bucket_name = record["s3"]["bucket"]["name"]
            file_name = record["s3"]["object"]["key"]
            file_size = record["s3"]["object"]["size"]

            # 拡張子取得
            if "." in file_name:
                file_extension = file_name.split(".")[-1].lower()
            else:
                file_extension = "unknown"

            # DynamoDBへ登録
            table.put_item(
                Item={
                    "FileName": file_name,
                    "BucketName": bucket_name,
                    "FileSize": file_size,
                    "FileExtension": file_extension,
                    "UploadTime": datetime.utcnow().isoformat()
                }
            )

            # CloudWatch Logs出力
            print(
                f"[INFO] File uploaded. "
                f"Bucket={bucket_name}, "
                f"File={file_name}, "
                f"Size={file_size} bytes"
            )

        return {
            "statusCode": 200,
            "body": json.dumps("File metadata registered successfully.")
        }

    except Exception as e:

        print(f"[ERROR] {str(e)}")

        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }
```
