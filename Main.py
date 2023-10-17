import os
import boto3
import botocore
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def uploadFolder(client, folder):
    try:
        # Validate that the folder exists
        if not os.path.exists(folder) or not os.path.isdir(folder):
            logger.error(f"Folder '{folder}' does not exist or is not a directory.")
            return

        files = []
        for dirpath, dirnames, filenames in os.walk(folder):
            for file in filenames:
                local_file = os.path.join(dirpath, file)
                # Use relative path as S3 key
                s3_key = os.path.relpath(local_file, folder).replace('\\', '/')
                logger.info(f"Uploading {s3_key}")
                client.upload_file(Filename=local_file, Bucket=bucket_name, Key=s3_key)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # AWS credentials and configuration
    access_key = 'XXXXXXXXXXXXXX' # Your Access Key -- Visit https://cockpit.fybe.com/account/security
    secret_key = 'XXXXXXXXXXXXXX' # Your Secret Key -- Visit https://cockpit.fybe.com/account/security
    s3_endpoint = 'https://ap-southeast-1.fybeobjects.com' # To check visit link https://cockpit.fybe.com/storage/object-storage/buckets
    bucket_name = 'EnterBucketName' # to check - https://cockpit.fybe.com/storage/object-storage/buckets

    # Initialize the S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=s3_endpoint,
        region_name='ap-southeast-1', # https://cockpit.fybe.com/storage/object-storage/buckets
        config=botocore.client.Config(signature_version='s3v4')
    )

    folder = input("Enter the name of the folder you want to sync: ")
    uploadFolder(s3, folder)
