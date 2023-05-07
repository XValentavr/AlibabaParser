import enum

import dotenv

envs = dotenv.dotenv_values()


class ProjectEnvs(str, enum.Enum):
    """
    Class to get all envs from dotenv file
    """

    WAIT: str = envs.get("TIME_WAIT")
    BASE_URL: str = envs.get("ALIBABA_BASE_URL")

    AMAZON_RAINFOREST_API: str = envs.get("AMAZON_RAINFOREST_API")
    AMAZON_RAINFOREST_BASE_URL: str = envs.get("AMAZON_RAINFOREST_BASE_URL")
    AMAZON_RAINFOREST_BASE_DOMAIN: str = envs.get("AMAZON_RAINFOREST_BASE_DOMAIN")

    AMAZON_AWS_HOST: str = envs.get("AMAZON_AWS_HOST")
    AMAZON_AWS_REGION: str = envs.get("AMAZON_AWS_REGION")
    AMAZON_AWS_API_ID: str = envs.get("AMAZON_AWS_API_ID")
    AMAZON_AWS_STAGE: str = envs.get("AMAZON_AWS_STAGE")
    AMAZON_AWS_ACCESS_KEY: str = envs.get("AMAZON_AWS_ACCESS_KEY")
    AMAZON_AWS_SECRET_KEY: str = envs.get("AMAZON_AWS_SECRET_KEY")
    POSTGRESQL_HOST: str = envs.get("POSTGRESQL_HOST")

    SELENIUM_WEBDRIVER_HOST: str = envs.get("SELENIUM_WEBDRIVER_HOST")

    GPT_API_KEY: str = envs.get("GPT_API_KEY")
    GPT_API_BASE_MODEL: str = envs.get("GPT_API_BASE_MODEL")

    ALIBABA_BASE_ENDPOINT: str = envs.get("ALIBABA_BASE_ENDPOINT")
    ALIBABA_BASE_API_KEY: str = envs.get("ALIBABA_BASE_API_KEY")
    ALIBABA_BASE_API_SECRET: str = envs.get("ALIBABA_BASE_API_SECRET")

    BITRIX_URL: str = envs.get('BITRIX_URL')

    CELERY_BROKER_URL: str = envs.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND_URL: str = envs.get('CELERY_RESULT_BACKEND_URL')

    def __str__(self) -> str:
        return "%s" % self.value
