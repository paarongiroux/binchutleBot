import boto3
import os


class BucketUploader:
    def __init__(self, bucket_name, access_key, secret_key, region):
        self.s3 = boto3.client("s3",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.bucket_name = bucket_name
        self.region = region

    def upload_image(self, file_path):
        file_name = os.path.basename(file_path)
        self.s3.upload_file(
            file_path,
            self.bucket_name,
            file_name,
            ExtraArgs={"ContentType": "image/png"}
        )
        return f"https://binchutlebot.s3.{self.region}.amazonaws.com/{file_name}"