from uuid import UUID

from pydantic import Field

from helpers.dtos.baseDTO import BaseModelDTO


class MostSimilarDTO(BaseModelDTO):
    id: UUID
    alibaba_source_id: UUID = Field(alias="alibabaSourceId")
    amazon_source_id: UUID = Field(alias="amazonSourceId")
    alibaba_source_link: str = Field(alias="alibabaSourceLink")
    amazon_source_link: str = Field(alias="amazonSourceLink")
    similarity: float
