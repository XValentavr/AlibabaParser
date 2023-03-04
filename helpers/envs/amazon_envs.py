import enum

import dotenv

envs = dotenv.dotenv_values()


class AmazonEnvs(str, enum.Enum):
    AMAZON_RAINFOREST_API = envs.get("AMAZON_RAINFOREST_API")
    AMAZON_RAINFOREST_BASE_URL = envs.get("AMAZON_RAINFOREST_BASE_URL")
    AMAZON_RAINFOREST_BASE_DOMAIN = envs.get("AMAZON_RAINFOREST_BASE_DOMAIN")

    def __str__(self):
        return "%s" % self.value
