import boto3
import os
import sys

def create_bucket():
    endpoint = os.environ.get("MLFLOW_S3_ENDPOINT_URL", "http://localhost:9000")
    key = os.environ.get("AWS_ACCESS_KEY_ID", "minioadmin")
    secret = os.environ.get("AWS_SECRET_ACCESS_KEY", "minioadmin")

    print(f"Connecting to S3 at {endpoint}...")
    s3 = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=key,
        aws_secret_access_key=secret,
    )

    bucket_name = "mlflow"
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except:
        print(f"Creating bucket '{bucket_name}'...")
        try:
            s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        except Exception as e:
            print(f"Failed to create bucket: {e}")
            sys.exit(1)

if __name__ == "__main__":
    create_bucket()
