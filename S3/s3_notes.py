
# boto3 offers two different styles of API - Resource API (high-level) and
# Client API (low-level). Client API maps directly to the underlying RPC-style
# service operations (put_object, delete_object, etc.). Resource API provides
# an object-oriented abstraction on top (object.delete(), object.put()).
#
# While Resource APIs may help simplify your code and feel more intuitive to
# some, others may prefer the explicitness and control over network calls
# offered by Client APIs. For new AWS customers, we recommend getting started
# with Resource APIs, if available for the service being used. At the time of
# writing they're available for Amazon EC2, Amazon S3, Amazon DynamoDB, Amazon
# SQS, Amazon SNS, AWS IAM, Amazon Glacier, AWS OpsWorks, AWS CloudFormation,
# and Amazon CloudWatch. This sample will show both styles.
#
# With no parameters or configuration, boto3 will look for access keys in these places:
#
#    1. Environment variables (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)
#    2. Credentials file (~/.aws/credentials or
#         C:\Users\USER_NAME\.aws\credentials)
#    3. AWS IAM role for Amazon EC2 instance
#       (http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)

import boto3
import uuid

# ------- Low-level Client API --------

# Connect to RPC client
s3client = boto3.client(service_name="s3")

# Create bucket in Tokyo Region, bucket name has to be globally unique
# Everything uploaded to Amazon S3 must belong to a bucket. These buckets are
# in the global namespace, and must have a unique name.
# For more information about bucket name restrictions, see:
# http://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html
bucket_name = 'is-globally-unique-{}'.format(uuid.uuid1())
s3client.create_bucket(Bucket=bucket_name,
                       CreateBucketConfiguration={"LocationConstraint": "ap-northeast-1"})

# Create object in the bucket, with name and content
# Files in Amazon S3 are called "objects" and are stored in buckets. A
# specific object is referred to by its key (i.e., name) and holds data.
s3client.put_object(Bucket=bucket_name, Key="Hello.txt", Body=b'Hello World!')


# Now the bucket is created, and you'll find it in your list of buckets.
list_buckets_resp = s3client.list_buckets()
for bucket in list_buckets_resp['Buckets']:
    if bucket['Name'] == bucket_name:
        print('(Just created) --> {} - there since {}'.format(
            bucket['Name'], bucket['CreationDate']))


# S3 pre-signed url: Securely share the object without making it publicly accessible.
# By default, the generated pre-signed URL will expire after one hour.
# You can change the expiration to be from 1 second to 604800 seconds (1 week).

# Buckets cannot be deleted unless they're empty.
