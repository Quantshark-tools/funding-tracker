from funding_tracker.shared.models.live_funding_point import LiveFundingPoint
from funding_tracker.shared.repositories.base import Repository


class LiveFundingPointRepository(Repository[LiveFundingPoint]):
    _model = LiveFundingPoint
