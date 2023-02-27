import enum

import dotenv

envs = dotenv.dotenv_values()


class AwsEnvs(str, enum.Enum):
    AMAZON_AWS_HOST = envs.get("AMAZON_AWS_HOST")
    AMAZON_AWS_REGION = envs.get('AMAZON_AWS_REGION')
    AMAZON_AWS_API_ID = envs.get('AMAZON_AWS_API_ID')
    AMAZON_AWS_STAGE = envs.get('AMAZON_AWS_STAGE')
    AMAZON_AWS_ACCESS_KEY = envs.get('AMAZON_AWS_ACCESS_KEY')
    AMAZON_AWS_SECRET_KEY = envs.get('AMAZON_AWS_SECRET_KEY')
