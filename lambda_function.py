# import json
# import boto3
# import os

# s3_client = boto3.client('s3')

# def lambda_handler(event, context):
#     log_data = event.get('log_data', None)
    
#     if log_data:
#         log_json = json.dumps(log_data)
#         bucket_name = os.environ['my-bucket-name']
#         object_key = 'server_logs.json'
        
#         s3_client.put_object(
#             Bucket=bucket_name,
#             Key=object_key,
#             Body=log_json
#         )
        
#         return {
#             'statusCode': 200,
#             'body': json.dumps('Log data successfully uploaded to S3!')
#         }
#     else:
#         return {
#             'statusCode': 400,
#             'body': json.dumps('No log data provided')
#         }
import boto3
import os

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'my-bucket-name'
    file_name = 'server_logs.json'
    file_path = file_name  # Lambda's writable directory is /tmp

    # If the file is already uploaded to Lambda, you can move it to S3
    try:
        s3.upload_file(file_path, bucket_name, file_name)
        return {
            'statusCode': 200,
            'body': f'File {file_name} uploaded to S3 bucket {bucket_name}'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
