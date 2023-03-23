# import boto3
# import uuid

# def lambda_handler(event, context):

#     # Get the S3 object and bucket name from the event
#     s3 = boto3.client('s3')
#     bucket_name = event['Records'][0]['s3']['bucket']['name']
#     object_key = event['Records'][0]['s3']['object']['key']

#     # Create a unique code to prefix the user bucket names
#     unique_code = str(uuid.uuid4())

#     # Create a log entry in a logfile on S3
#     log_entry = f"File {object_key} was uploaded to {bucket_name}."
#     log_bucket_name = "cis4010assignment3e"
#     log_object_key = f"logfile/{unique_code}/{object_key}.txt"
#     s3.put_object(Bucket=log_bucket_name, Key=log_object_key, Body=log_entry)

#     # Get the list of users from a distribution list maintained on S3
#     users_bucket_name = "your-users-bucket-name"
#     users_object_key = "distribution-list/users.txt"
#     users = s3.get_object(Bucket=users_bucket_name, Key=users_object_key)['Body'].read().decode('utf-8').split()

#     # Copy the file to each user's bucket
#     for user in users:
#         user_bucket_name = f"{unique_code}-{user}"
#         s3.copy_object(Bucket=user_bucket_name, CopySource={'Bucket': bucket_name, 'Key': object_key}, Key=object_key)

import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


# Commands to run this bad boy
# aws ecr create-repository --repository-name my-lambda-image --image-scanning-configuration scanOnPush=true
# docker tag my-lambda-image:latest 774766912133.dkr.ecr.ca-central-1.amazonaws.com/my-lambda-image:latest
# aws ecr get-login-password --region ca-central-1 | docker login --username AWS --password-stdin 774766912133.dkr.ecr.ca-central-1.amazonaws.com
# docker push 774766912133.dkr.ecr.ca-central-1.amazonaws.com/my-lambda-image:latest
# aws lambda create-function --function-name my-lambda-function --package-type Image --code ImageUri=774766912133.dkr.ecr.ca-central-1.amazonaws.com/my-lambda-image:latest --role arn:aws:iam::774766912133:role/service-role/nodePartA-role-le7kslnb
