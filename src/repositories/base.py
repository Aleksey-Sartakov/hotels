from pydantic import BaseModel
from sqlalchemy import select, update, delete


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)

        return [self.schema.model_validate(entity) for entity in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        entity = result.scalars().one_or_none()
        if entity:
            entity = self.schema.model_validate(entity)

        return entity

    async def add(self, data: BaseModel):
        entity = self.model(**data.model_dump())
        self.session.add(entity)
        await self.session.flush()

        return self.schema.model_validate(entity)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(stmt)

    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
