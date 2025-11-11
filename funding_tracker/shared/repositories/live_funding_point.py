from funding_tracker.shared.models.live_funding_point import LiveFundingPoint
from funding_tracker.shared.repositories.base import Repository


class LiveFundingPointRepository(Repository[LiveFundingPoint]):
    """Repository for managing live unsettled funding rate records."""

    _model = LiveFundingPoint
