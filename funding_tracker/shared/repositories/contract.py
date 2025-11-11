from funding_tracker.shared.models.contract import Contract
from funding_tracker.shared.repositories.base import Repository


class ContractRepository(Repository[Contract]):
    """Repository for managing perpetual futures contracts."""

    _model = Contract
