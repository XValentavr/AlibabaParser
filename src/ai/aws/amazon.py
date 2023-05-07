import json
import logging
from typing import Dict

import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth

from helpers.init_logger import create_logger
from helpers.project_envs import ProjectEnvs


class AmazonAI:
    """
    Class to work wit AWS AI solution kit
    """

    def __init__(self):
        self.base_url = (
            f"https://{ProjectEnvs.AMAZON_AWS_API_ID}.execute-api."
            f"{ProjectEnvs.AMAZON_AWS_REGION}.amazonaws.com/{ProjectEnvs.AMAZON_AWS_STAGE}/"
        )
        self.__logger = create_logger()

    @staticmethod
    def __authorize() -> AWSRequestsAuth:
        """
        Authorize yourself on AWS
        :return: auth instance
        """
        return AWSRequestsAuth(
            aws_access_key=ProjectEnvs.AMAZON_AWS_ACCESS_KEY,
            aws_secret_access_key=ProjectEnvs.AMAZON_AWS_SECRET_KEY,
            aws_host=ProjectEnvs.AMAZON_AWS_HOST,
            aws_region=ProjectEnvs.AMAZON_AWS_REGION,
            aws_service="execute-api",
        )

    def __make_request(self, url: str, payload: Dict, method: str = 'POST'):
        """
        Make main request to AWS Lambda
        :param url: url to send response
        :param payload: data to compare
        :param method: method to use (get default)
        :return: response status or data
        """
        try:
            return requests.request(method=method, url=url, data=json.dumps(payload), auth=self.__authorize())
        except Exception:
            self.__logger.setLevel(logging.DEBUG)

    def image_similarity(
            self,
            image_amazon_url: str = None,
            image_alibaba_url: str = None,
            end: str = "image-similarity",
    ) -> float:
        """
        Get image similarity from AWS
        :param image_amazon_url: amazon image url
        :param image_alibaba_url: alibaba image url
        :param end: end of endpoint
        :return: image similarity
        """
        url = self.base_url + end
        payload = {"url_1": image_amazon_url, "url_2": image_alibaba_url}
        response = self.__make_request(url, payload)
        if response:
            similarity = json.loads(response.text)
            return similarity

    def text_similarity(self,
                        amazon_keywords: str = None,
                        alibaba_keywords: str = None,
                        end: str = ''):
        """
        Get text similarity from AWS
        :param amazon_keywords:  amazon keywords
        :param alibaba_keywords: alibaba keywords
        :param end: end of endpoint
        :return: text similarity
        """

        url = self.base_url + end
        payload = {"text_1": amazon_keywords, "text_2": alibaba_keywords}
        response = self.__make_request(url, payload)
        if response:
            similarity = json.loads(response.text)
            return similarity


amazon_ai = AmazonAI()
