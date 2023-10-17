import os
import boto3
import botocore
import logging
import csv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def file_size(path):
    return os.path.getsize(path)

def uploadFolder(client, folder, make_public):
    uploaded_files = []

    try:
        # Validate that the folder exists
        if not os.path.exists(folder) or not os.path.isdir(folder):
            logger.error(f"Folder '{folder}' does not exist or is not a directory.")
            return

        for dirpath, dirnames, filenames in os.walk(folder):
            for file in filenames:
                local_file = os.path.join(dirpath, file)
                # Use relative path as S3 key
                s3_key = os.path.relpath(local_file, folder).replace('\\', '/')

                # Check if the file exists in the S3 bucket and has the same size
                try:
                    s3_object = client.head_object(Bucket=bucket_name, Key=s3_key)
                    if s3_object['ContentLength'] == file_size(local_file):
                        logger.info(f"Skipping {s3_key} (already exists with the same size)")
                        continue
                except client.exceptions.ClientError as e:
                    # Object does not exist, proceed with the upload
                    if e.response['Error']['Code'] == '404':
                        pass
                    else:
                        raise e

                # Upload the file
                logger.info(f"Uploading {s3_key}")
                client.upload_file(Filename=local_file, Bucket=bucket_name, Key=s3_key)

                # Set ACL based on user input
                if make_public:
                    client.put_object_acl(Bucket=bucket_name, Key=s3_key, ACL='public-read')
                else:
                    client.put_object_acl(Bucket=bucket_name, Key=s3_key, ACL='private')

                # Construct and store the URL of the uploaded file
                file_url = f"{s3_endpoint}/{bucket_name}/{s3_key}"
                uploaded_files.append((s3_key, file_url))

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    return uploaded_files

def save_links_to_csv(uploaded_files, csv_filename):
    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['File Name', 'File URL'])
        for key, url in uploaded_files:
            csv_writer.writerow([key, url])

if __name__ == "__main__":
    # AWS credentials and configuration
    access_key = 'XXXXX'
    secret_key = 'XXXXXXX'
    s3_endpoint = 'https://ap-southeast-1.fybeobjects.com'
    bucket_name = 'BucketNameHere'

    # Initialize the S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=s3_endpoint,
        region_name='ap-southeast-1',
        config=botocore.client.Config(signature_version='s3v4')
    )

    folder = input("Enter the name of the folder you want to sync: ")
    make_public = input("Do you want to make the uploaded files public? (yes/no): ").lower() == 'yes'

    uploaded_files = uploadFolder(s3, folder, make_public)

    # Share the list of uploaded files and their links
    if uploaded_files:
        print("Uploaded Files:")
        for key, url in uploaded_files:
            print(f"{key}: {url}")

        # Save the links to a CSV file
        csv_filename = 'uploaded_files.csv'
        save_links_to_csv(uploaded_files, csv_filename)
        print(f"Links saved to {csv_filename}")
