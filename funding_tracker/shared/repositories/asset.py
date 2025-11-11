from funding_tracker.shared.models.asset import Asset
from funding_tracker.shared.repositories.base import Repository


class AssetRepository(Repository[Asset]):
    """Repository for managing cryptocurrency assets."""

    _model = Asset
