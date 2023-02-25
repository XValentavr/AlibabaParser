import enum

import dotenv

envs = dotenv.dotenv_values()


class AlibabaEnvs(str, enum.Enum):
    BASE_URL = envs.get("ALIBABA_BASE_URL")
