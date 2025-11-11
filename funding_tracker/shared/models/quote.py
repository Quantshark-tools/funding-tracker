from funding_tracker.shared.models.base import NameModel


class Quote(NameModel, table=True):
    """Quote currency (e.g., USD, USDT)."""
    ...
