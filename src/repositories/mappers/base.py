from src.database import Base
from src.schemas.base import BaseSchema


class DataMapper:
    db_model: type[Base] = None
    schema: type[BaseSchema] = None

    @classmethod
    def map_to_domain_entity(cls, data: Base) -> BaseSchema:
        return cls.schema.model_validate(data)

    @classmethod
    def map_to_persistence_entity(cls, data: BaseSchema) -> Base:
        return cls.db_model(**data.model_dump())
