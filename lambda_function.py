import json
import boto3
import os

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    log_data = event.get('log_data', None)
    
    if log_data:
        log_json = json.dumps(log_data)
        bucket_name = os.environ['log-bucket-practice2']
        object_key = 'server_logs.json'
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=log_json
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Log data successfully uploaded to S3!')
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('No log data provided')
        }
