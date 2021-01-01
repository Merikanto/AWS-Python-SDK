import boto3
from botocore.exceptions import ClientError

import uuid
import logging
from pip._vendor.distlib.compat import raw_input


# ------- Resource API, Object-based --------

# Connect to S3 Resource API
s3 = boto3.resource("s3")

# Create bucket in Tokyo Region, bucket name has to be globally unique
bucket_name = "test-{}".format(uuid.uuid1())
s3.create_bucket(Bucket=bucket_name,
                 CreateBucketConfiguration={"LocationConstraint": "ap-northeast-1"})

# Create object under a folder, and copy content from another file
# Note: NO kwargs for Bucket & Key
# Source & Destination file type must be the same, otherwise will be unreadable (binary)
body = open("S3.pdf", "rb")
key = "Result/Converted.pdf"
s3.Object(bucket_name, key).put(Body=body)


# Generate a pre-signed URL for external access, using Client API
# Resource API does not have attribute for generating pre-signed url
def created_pre_signed_url():

    s3client = boto3.client("s3")
    try:
        url = s3client.generate_presigned_url("get_object", {"Bucket": bucket_name, "Key": key})
        print("\nUploaded a local PDF file to S3.")
        print("\nTry this pre-signed url to access the object temporarily:\n" + url)
    except ClientError as e:
        logging.error(e)
        return None

    return url


created_pre_signed_url()


# Create a bucket & object object
bucket = s3.Bucket(bucket_name)
obj = bucket.Object(key)

# Add input to proceed to next step
try:
    type_input = raw_input
except NameError:
    pass
input("\nPress Enter to delete all objects and the bucket:")


# Delete bucket
# First delete all objects to make sure bucket is empty, then delete empty bucket
for key in bucket.objects.all():
    key.delete()
bucket.delete()





