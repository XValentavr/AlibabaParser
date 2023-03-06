import urllib.request
import boto3
from boto3 import Session

from helpers.envs.project_envs import ProjectEnvs


class AmazonS3Client:
    def __init__(self):
        self.path = ProjectEnvs.AMAZON_AWS_S3_BASE_PATH
        self.file = self.path + "test.png"
        self.bucket = ProjectEnvs.AMAZON_AWS_S3_BUCKET
        self.bucket_key = "test.png"

    def image_s3_worker(self, image: str) -> None:
        self.__save_locally(image)

    def __init_s3_client(self) -> Session:
        return boto3.Session(
            aws_access_key_id=ProjectEnvs.AMAZON_AWS_ACCESS_KEY,
            aws_secret_access_key=ProjectEnvs.AMAZON_AWS_SECRET_KEY,
        )

    def __save_locally(self, image: str) -> None:
        urllib.request.urlretrieve(image, self.file)

    def __save_to_s3(self) -> None:
        s3_client = self.__init_s3_client().resource("s3")
        s3_bucket = s3_client.Bucket(self.bucket)

        s3_bucket.meta.client.upload_file(
            self.file, self.bucket, self.bucket_key, ExtraArgs={"ACL": "public-read"}
        )

    def __get_from_s3(self, s3) -> None:
        ...

    def _delete_from_s3(self) -> None:
        ...
