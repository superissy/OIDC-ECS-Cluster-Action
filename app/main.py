import boto3
import json
import datetime

dynamodb = boto3.client("dynamodb")

table_name = "test-table"

date_time = datetime.datetime.now()

backup_name = f"{table_name}-snapshot-{date_time.strftime('%Y-%m-%d-%H-%M-%S')}"

response = dynamodb.describe_table(TableName=table_name)
backup_response = dynamodb.create_backup(
    TableName=table_name,
    BackupName=backup_name
)
print("+++++++++++++++")
print(response)
print("+++++++++++++++")
print(backup_response)
print(date_time)


tb = 'arn:aws:dynamodb:us-east-1:438270576332:table/test-table'
new_tb = tb.split("/")[-1]
print(new_tb)