import boto3
from datetime import datetime

aws_access_key_id = "x"
aws_secret_access_key = "x"
client_res = boto3.resource('s3', region_name='ca-central-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
client = boto3.client('s3', region_name='ca-central-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def lambda_handler(event, context):

    logFileBody = ""

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
        logFileBody += "Found new file: " + newFilekey + "\n"
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


    #Create the logfile bucket if it doesn't exist
    logFileBucketName = "imckechnlogs"
    try:
        client_res.meta.client.head_bucket(Bucket=logFileBucketName)
    except:
        client.create_bucket(
            Bucket=logFileBucketName,
            CreateBucketConfiguration={
                'LocationConstraint': 'ca-central-1',
            },
        )


    #Get the subscription list
    subscriptionList = client.get_object(Bucket='subscribercollectionianmckechnie', Key='subscribers')
    subs = subscriptionList['Body'].read()

    for subBucket in subs.splitlines():
        try:
            subBucket = subBucket.decode()

            #Check if the bucket exists, if not, create it
            try:
                client_res.meta.client.head_bucket(Bucket=subBucket)
            except:
                client.create_bucket(
                    Bucket=subBucket,
                    CreateBucketConfiguration={
                        'LocationConstraint': 'ca-central-1',
                    },
                )

            #Copy the s3 object over to the subscriber
            client_res.meta.client.copy(copy_source, subBucket, newFilekey)
            logFileBody += "Copied file to " + subBucket + "\n"

        except:
            logFileBody += "Error copying file to " + subBucket + "\n"



    #Write the logfile
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    time = current_time.replace(":", "")
    logFileKey = time + ".log"

    object = client_res.Object(
        bucket_name=logFileBucketName,
        key=logFileKey
    )

    object.put(Body=logFileBody)
