import boto3
from botocore.exceptions import ClientError
import logging


class S3SERVICE(object):

    def __init__(self, aws_access_key_id, aws_secret_access_key, region):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region
        self.session = boto3.Session(aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key,
                                     region_name=region)
        self.s3 = self.session.resource('s3')

    def upload_fileobj(self, file_name=None, bucket=None, key=None):
        if (key is None) or (bucket is None):
            logging.info("key and bucket cannot be None")
            return False
        s3_client = boto3.client('s3')
        try:
            s3_client.upload_fileobj(file_name, bucket, key)
            logging.info("File object uploaded to https://s3.amazonaws.com/{}/{}".format(bucket, key))

        except ClientError as e:
            logging.info("INFO: Failed to upload image")
            logging.error(e)
            return False
        return True