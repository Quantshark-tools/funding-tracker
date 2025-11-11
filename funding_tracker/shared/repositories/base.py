from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

M = TypeVar("M", bound=SQLModel)


class Repository[M]:
    """Base repository class providing session access and common operations."""

    _model: type[M]

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, record: M) -> M:
        """Add a single record to the database.

        Args:
            record: Model instance to add

        Returns:
            The added model instance with any database-generated fields populated
        """
        self._session.add(record)
        await self._session.flush()
        return record
