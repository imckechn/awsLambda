import json
import boto3

aws_access_key_id = X
aws_secret_access_key = X
client_res = boto3.resource('s3', region_name='ca-central-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
client = boto3.client('s3', region_name='ca-central-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def lambda_handler(event, context):

    # Get the object from the event and show its content type
    newFilebucket = event['Records'][0]['s3']['bucket']['name']
    newFilekey = event['Records'][0]['s3']['object']['key']

    copy_source = {
        'Bucket': newFilebucket,
        'Key': newFilekey
    }

    try:
        newFileUploaded = client.get_object(Bucket=newFilebucket, Key=newFilekey)
        print("CONTENT TYPE: " + newFileUploaded['ContentType'])
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    #Get the subscription list
    subscriptionList = client.get_object(Bucket='subscribercollectionianmckechnie', Key='subscribers')

    subs = subscriptionList.get()['Body'].read()

    for sub in subs.splitlines():
        print(sub)
        #Send the email
        client.meta.client.copy(copy_source, sub, newFilekey)

