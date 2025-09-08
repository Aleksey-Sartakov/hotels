from sqlalchemy import select

from src.models.hotels import Hotels
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = Hotels

    async def get_all(self, location, title, limit, offset):
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
        hotels = result.scalars().all()

