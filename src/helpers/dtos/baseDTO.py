from typing import Any

from pydantic import BaseModel


class BaseModelDTO(BaseModel):
    @classmethod
    def from_orm(cls, obj: Any, **kwargs) -> Any:
        for field in kwargs:
            setattr(obj, field, kwargs[field])
        return super().from_orm(obj)

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        validate_assignment = True
        use_enum_values = False
