from quantshark_shared.models.asset import Asset

from funding_tracker.db.repositories.base import Repository


class AssetRepository(Repository[Asset]):
    _model = Asset
