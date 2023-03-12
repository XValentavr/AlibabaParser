import enum

import dotenv

envs = dotenv.dotenv_values()


class ProjectEnvs(str, enum.Enum):
    WAIT: str = envs.get("TIME_WAIT")
    BASE_IMAGE_URL: str = envs.get("BASE_IMAGE_URL")
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
    POSTGRESQL_HOST: str = envs.get('POSTGRESQL_HOST')

    def __str__(self) -> str:
        return "%s" % self.value
