import enum


class CeleryStatusEnum(str, enum.Enum):
    """
    Need to specify which table myst be cleared
    """

    SUCCESS: str = "SUCCESS"
    FAILURE: str = "FAILURE"
