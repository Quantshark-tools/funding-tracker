from uuid import UUID

from sqlalchemy.sql.expression import select

from funding_tracker.shared.models.historical_funding_point import HistoricalFundingPoint
from funding_tracker.shared.repositories.base import Repository


class HistoricalFundingPointRepository(Repository[HistoricalFundingPoint]):
    _model = HistoricalFundingPoint

    async def get_oldest_for_contract(
        self, contract_id: UUID
    ) -> HistoricalFundingPoint | None:
        stmt = (
            select(HistoricalFundingPoint)
            .where(HistoricalFundingPoint.contract_id == contract_id)
            .order_by(HistoricalFundingPoint.timestamp.asc())
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_newest_for_contract(
        self, contract_id: UUID
    ) -> HistoricalFundingPoint | None:
        stmt = (
            select(HistoricalFundingPoint)
            .where(HistoricalFundingPoint.contract_id == contract_id)
            .order_by(HistoricalFundingPoint.timestamp.desc())
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
