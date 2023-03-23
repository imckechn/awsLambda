import json
import boto3

aws_access_key_id = "x"
aws_secret_access_key = "x"
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

    subs = subscriptionList['Body'].read()

    for subBucket in subs.splitlines():
        subBucket = subBucket.decode()

        #Check if the bucket exists, if not, create it
        print("bucket =", subBucket)
        try:
            client_res.meta.client.head_bucket(Bucket=subBucket)
        except:
            client.create_bucket(
                Bucket='subBucket',
                CreateBucketConfiguration={
                    'LocationConstraint': 'ca-central-1',
                },
            )

        #Copy the s3 object over to the subscriber
        client_res.meta.client.copy(copy_source, subBucket, newFilekey)