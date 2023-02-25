import enum

import dotenv

envs = dotenv.dotenv_values()


class CssClasses(str, enum.Enum):
    LIST_ITEM = 'list-item'
    DECLARATIVE = 'declarative'
    IMAGE_WRAPPER = 'imgTagWrapper'
    MAIN_IMAGE = 'dynamic-image a-stretch-horizontal'
    LAYOUTS = 'regularAltImageViewLayout'
