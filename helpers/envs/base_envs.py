import enum

import dotenv

envs = dotenv.dotenv_values()


class BaseEnvs(str, enum.Enum):
    WAIT = envs.get("TIME_WAIT")
