from funding_tracker.shared.models.historical_funding_point import HistoricalFundingPoint
from funding_tracker.shared.repositories.base import Repository


class HistoricalFundingPointRepository(Repository[HistoricalFundingPoint]):
    """Repository for managing historical settled funding rate records."""

    _model = HistoricalFundingPoint
