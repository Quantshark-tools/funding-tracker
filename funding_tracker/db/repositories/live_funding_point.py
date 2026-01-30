from quantshark_shared.models.live_funding_point import LiveFundingPoint

from funding_tracker.db.repositories.base import Repository


class LiveFundingPointRepository(Repository[LiveFundingPoint]):
    _model = LiveFundingPoint
