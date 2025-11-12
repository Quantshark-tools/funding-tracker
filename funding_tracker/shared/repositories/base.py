from collections.abc import Iterable
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

from funding_tracker.shared.repositories.utils import bulk_insert

M = TypeVar("M", bound=SQLModel)


class Repository[M]:
    _model: type[M]

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, record: M) -> M:
        self._session.add(record)
        await self._session.flush()
        return record

    async def bulk_insert_ignore(self, records: Iterable[M]) -> None:
        """Inserts records, ignoring conflicts."""
        await bulk_insert(
            self._session,
            self._model,
            records,
            on_conflict="ignore",
        )
