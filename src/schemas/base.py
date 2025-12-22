from pydantic import BaseModel, ConfigDict, model_validator


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NonEmptyPayloadSchema(BaseSchema):
    @model_validator(mode='before')
    def require_at_least_one_key(cls, values):
        if not values:
            raise ValueError("Передано пустое тело запроса. Как минимум одно поле должно быть указано")

        return values
