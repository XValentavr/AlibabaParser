import json

import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth

from helpers.envs.aws_envs import AwsEnvs


class AmazonAI:

    def __init__(self):
        self.base_url = f'https://{AwsEnvs.AMAZON_AWS_API_ID}.execute-api.{AwsEnvs.AMAZON_AWS_REGION}.amazonaws.com/{AwsEnvs.AMAZON_AWS_STAGE}/'

    @staticmethod
    def __authorize():
        return AWSRequestsAuth(
            aws_access_key=AwsEnvs.AMAZON_AWS_ACCESS_KEY,
            aws_secret_access_key=AwsEnvs.AMAZON_AWS_SECRET_KEY,
            aws_host=AwsEnvs.AMAZON_AWS_HOST,
            aws_region=AwsEnvs.AMAZON_AWS_REGION,
            aws_service='execute-api')

    def image_similarity(self, image_amazon_url=None, image_alibaba_url=None, end='image-similarity-ml'):
        url = self.base_url + end
        payload = {
            'url_1': image_amazon_url,
            'url_2': image_alibaba_url
        }

        response = requests.request("POST", url, data=json.dumps(payload), auth=self.__authorize())
        similarity = json.loads(response.text)
        return similarity


amazon_ai = AmazonAI()
