from sqlalchemy import select

from src.models.hotels import Hotels
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = Hotels
    schema = Hotel

    async def get_all(self, location, title, limit, offset) -> list[schema]:
        query = select(self.model)
        if location:
            query = query.filter(Hotels.location.icontains(location))
        if title:
            query = query.filter(Hotels.title.icontains(title))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [self.schema.model_validate(hotel) for hotel in result.scalars().all()]
