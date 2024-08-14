# Team5-DE
Assignment:
SERVERLESS LOG DATA PROCESSING PIPELINE

Project Overview <br/>
This project builds a serverless data processing pipeline for analysing server logs stored in JSON format. The pipeline uses AWS services Lambda, S3, Glue, and CloudWatch. The project includes:<br/>
Ingesting log data using a Lambda function. <br/>
Storing the data in an S3 bucket.<br/>
Cataloging the data using AWS Glue Crawler.<br/>
Processing the data with an AWS Glue ETL job.<br/>
Monitoring the Glue job using CloudWatch with custom alarms.<br/>

Technologies Used:<br/>
AWS CLI<br/>
AWS Lambda<br/>
AWS S3<br/>
AWS CloudWatch<br/>
AWS Glue<br/>
Python<br/>

Use Case: <br/>
The primary use case is to process server logs and extract error logs, which are logs with status codes indicating errors (status codes 400–599). The extracted error logs are then used to monitor the application's performance and raise alarms when error count exceeds given thresholds.<br/>

Prerequisites:<br/>
Install AWS CLI.<br/>
Python environment (VS Code) for server-log data generation, lambda function and etl-job development.<br/>

Implementation (step by step): <br/>

DATA INGESTION AND POLICIES:<br/>
1.Write a python script to randomly generate 100 server logs which will become our data to process. Refer server_logs_generation.py and server_logs.json.<br/>
2.Create IAM user and access keys. Use those keys to configure aws in the CLI using command<br/>
'''
aws configure
'''
3.Create roles for lambda and glue using trust-policy-lambda.json and trust-policy-glue.json files with the commands<br/>
aws iam create-role --role-name LambdaS3Role --assume-role-policy-document file://trust-policy-lambda.json<br/>
aws iam create-role --role-name GlueS3Role --assume-role-policy-document file://trust-policy-glue.json<br/>
4.Attach role policies with full S3 and cloudwatch access.<br/>
aws iam attach-role-policy --role-name LambdaS3Role --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess<br/>
aws iam attach-role-policy --role-name GlueS3Role --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess<br/>
aws iam attach-role-policy --role-name LambdaS3Role --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess<br/>
aws iam attach-role-policy --role-name GlueS3Role --policy-arn arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole<br/>
5.Create an S3 bucket with a proper name.<br/>
aws s3 mb s3://my-bucket-name<br/>
6.Write a lambda function to collect data from server_logs.json and load it into S3. Refer lambda_function.py. <br/>
7.Now zip the function and data file using the command and create the folder name to LogIngestionFunction and update the lambda handler to python 3.8. <br/>
zip function.zip lambda_function.py server_logs.json<br/>
aws lambda create-function --function-name LogIngestionFunction --zip-file fileb://function.zip --handler lambda_function.lambda_handler --runtime python3.8 --role arn:aws:iam::ACCOUNT ID:role/LambdaS3Role<br/>
8.Use test_event.json file to invoke lambda function and save the response into response.json.<br/>
aws lambda invoke --function-name ProcessServerLogs \<br/>                                                 
    --payload file://test_event.json \<br/>
    response.json<br/>
aws lambda invoke --function-name LogIngestionFunction response.json<br/>

DATA CATALOGING:<br/>
9.Create a database in the glue. Choose a name.<br/>
aws glue create-database --database-input "{\"Name\":\"my-database\"}"<br/>
10.Create and configure the crawler with crawler_config.json file.<br/>
aws glue create-crawler --cli-input-json file://crawler_config.json<br/>
11.Start the crawler for cataloging.<br/>
aws glue start-crawler --name server-logs-crawler<br/>

DATA PROCESSING USING GLUE ETL JOB:<br/>
12.Write a glue_etl_script.py to process the error logs and copy to S3 bucket.<br/>
aws s3 cp glue_etl_script.py s3://my-bucket-name/glue_etl_script.py<br/>
13.Create and configure the etl-job using glue_job_config.json file.<br/>
aws glue create-job --cli-input-json file://etl_job_config.json<br/>
14.Start the job run with the name assigned using the config file.<br/>
aws glue start-job-run --job-name error-log-analysis-job<br/>
After running the etl-job successfully, processed error logs are stored in the S3 bucket in the json format.<br/>

MONITORING AND ALARMS:








