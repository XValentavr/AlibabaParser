import enum


class TableModelsEnum(str, enum.Enum):
    """
    Need to specify which table myst be cleared
    """

    ALIBABA: str = "alibaba"
    AMAZON: str = "amazon"
