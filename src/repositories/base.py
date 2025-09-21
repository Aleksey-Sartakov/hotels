from pydantic import BaseModel
from sqlalchemy import select, update, delete, insert

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filters, **filters_by):
        query = (
            select(self.model)
            .filter_by(**filters_by)
            .filter(*filters)
        )
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(entity) for entity in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        entity = result.scalars().one_or_none()
        if entity:
            entity = self.mapper.map_to_domain_entity(entity)

        return entity

    async def add(self, data: BaseModel):
        entity = self.model(**data.model_dump())
        self.session.add(entity)
        await self.session.flush()

        return self.mapper.map_to_domain_entity(entity)

    async def add_bulk(self, data: list[BaseModel]):
        stmt = (
            insert(self.model)
            .values([item.model_dump() for item in data])
        )
        await self.session.execute(stmt)

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
