import json

import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth

from src.helpers.project_envs import ProjectEnvs


class AmazonAI:
    def __init__(self):
        self.base_url = (
            f"https://{ProjectEnvs.AMAZON_AWS_API_ID}.execute-api."
            f"{ProjectEnvs.AMAZON_AWS_REGION}.amazonaws.com/{ProjectEnvs.AMAZON_AWS_STAGE}/"
        )

    @staticmethod
    def __authorize() -> AWSRequestsAuth:
        return AWSRequestsAuth(
            aws_access_key=ProjectEnvs.AMAZON_AWS_ACCESS_KEY,
            aws_secret_access_key=ProjectEnvs.AMAZON_AWS_SECRET_KEY,
            aws_host=ProjectEnvs.AMAZON_AWS_HOST,
            aws_region=ProjectEnvs.AMAZON_AWS_REGION,
            aws_service="execute-api",
        )

    def image_similarity(
        self,
        image_amazon_url: str = None,
        image_alibaba_url: str = None,
        end: str = "image-similarity",
    ) -> float:
        url = self.base_url + end
        payload = {"url_1": image_amazon_url, "url_2": image_alibaba_url}

        response = requests.request(
            "POST", url, data=json.dumps(payload), auth=self.__authorize()
        )
        similarity = json.loads(response.text)
        return similarity


amazon_ai = AmazonAI()
