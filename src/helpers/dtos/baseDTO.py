from typing import Any

from pydantic import BaseModel


class BaseModelDTO(BaseModel):
    """
    Class to work with pydantic dtos
    """

    @classmethod
    def from_orm(cls, obj: Any, **kwargs) -> Any:
        """
        override main pydantic from_orm method
        :param obj: income pydantic objects
        :param kwargs: more arguments
        :return: overrided method
        """
        for field in kwargs:
            setattr(obj, field, kwargs[field])
        return super().from_orm(obj)

    class Config:
        """
        Inner class to configure pydantic models
        """

        allow_population_by_field_name = True
        orm_mode = True
        validate_assignment = True
        use_enum_values = False
