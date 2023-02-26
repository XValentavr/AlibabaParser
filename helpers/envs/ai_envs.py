import enum

import dotenv

envs = dotenv.dotenv_values()


class AIEnvs(str, enum.Enum):
    BASE_IMAGE_URL = envs.get("BASE_IMAGE_URL")
