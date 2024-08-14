import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col
import boto3

# Retrieve job parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read data from AWS Glue Data Catalog
log_df = glueContext.create_dynamic_frame.from_catalog(
    database="my-database",
    table_name="server_logs_my_data_bucket"
)

# Convert DynamicFrame to Spark DataFrame
log_spark_df = log_df.toDF()

# Filter error logs (status_code between 400 and 599)
error_logs = log_spark_df.filter((col("status_code") >= 400) & (col("status_code") < 600))

# Count the number of error logs
error_count = error_logs.count()

# Send custom metric to CloudWatch
cloudwatch = boto3.client('cloudwatch')
cloudwatch.put_metric_data(
    Namespace='GlueETL',
    MetricData=[
        {
            'MetricName': 'ErrorLogCount',
            'Dimensions': [
                {
                    'Name': 'JobName',
                    'Value': args['JOB_NAME']
                },
            ],
            'Unit': 'Count',
            'Value': error_count
        },
    ]
)

# Write the filtered error logs back to S3 in JSON format
error_logs.write.mode('overwrite').json("s3://my-data-bucket/error-logs.json")

# Complete the job
job.commit()
# # # import sys
# # # from awsglue.context import GlueContext
# # # from pyspark.context import SparkContext
# # from pyspark.sql.functions import col, count

# # # sc = SparkContext()
# # # glueContext = GlueContext(sc)
# # # spark = glueContext.spark_session

# # # # Load data from Glue catalog
# # # data_frame = glueContext.create_dynamic_frame.from_catalog(database = "my_database", table_name = "server_logs_my_data_bucket").toDF()

# # # # Filter error logs
# # # error_logs = data_frame.filter((col("status_code") >= 400) & (col("status_code") < 600))

# # # # Aggregate error counts
# # # error_counts = error_logs.groupBy("request").agg(count("status_code").alias("error_count"))

# # # # Write results to S3
# # # error_counts.write.mode("overwrite").json("s3://my-data-bucket/error-log-analysis/")
# # import sys
# # from awsglue.transforms import *
# # from awsglue.utils import getResolvedOptions
# # from pyspark.context import SparkContext
# # from awsglue.context import GlueContext
# # from awsglue.job import Job

# # # Retrieve job parameters
# # args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# # # # Initialize Spark and Glue contexts
# # sc = SparkContext()
# # glueContext = GlueContext(sc)
# # spark = glueContext.spark_session
# # job = Job(glueContext)
# # job.init(args['JOB_NAME'], args)

# # # Read data from AWS Glue Data Catalog
# # log_df = glueContext.create_dynamic_frame.from_catalog(database = "my-database", table_name = "server_logs_my_data_bucket")
# # #log_df.show()  # Display the data
# # # Filter error logs
# # log_df.columns()
# # #error_logs = log_df.filter((col("status_code") >= 400) & (col("status_code") < 600))

# # # Aggregate error counts
# # #error_counts = error_logs.groupBy("request").agg(count("status_code").alias("error_count"))

# # # Write results to S3
# # #error_counts.write.mode("overwrite").json("s3://my-data-bucket/error-counts")


# # # log_df.toDF().write.mode('overwrite').json("s3://my-data-bucket/example.json")
# # #error_logs.toDF().write.mode('overwrite').json("s3://my-data-bucket/error-logs.json")
# # # Commit the job
# # job.commit()
# import sys
# from awsglue.transforms import *
# from awsglue.utils import getResolvedOptions
# from pyspark.context import SparkContext
# from awsglue.context import GlueContext
# from awsglue.job import Job
# from pyspark.sql.functions import col  # Import necessary function for filtering

# # Retrieve job parameters
# args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# # Initialize Spark and Glue contexts
# sc = SparkContext()
# glueContext = GlueContext(sc)
# spark = glueContext.spark_session
# job = Job(glueContext)
# job.init(args['JOB_NAME'], args)

# # Read data from AWS Glue Data Catalog
# log_df = glueContext.create_dynamic_frame.from_catalog(
#     database="my-database",
#     table_name="server_logs_my_data_bucket"
# )

# # Convert DynamicFrame to Spark DataFrame
# log_spark_df = log_df.toDF()

# # Filter error logs (status_code between 400 and 599)
# error_logs = log_spark_df.filter((col("status_code") >= 400) & (col("status_code") < 600))

# # Write the filtered error logs back to S3 in JSON format
# error_logs.write.mode('overwrite').json("s3://my-data-bucket/error-logs.json")

# # Complete the job
# job.commit()
