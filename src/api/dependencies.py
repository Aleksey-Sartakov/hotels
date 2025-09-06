from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field


class Pagination(BaseModel):
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=3, ge=1, le=100)


PaginationDep = Annotated[Pagination, Depends()]
