"""Exchange adapter protocol.

Adapters implement required methods without explicit inheritance.
"""

from datetime import datetime
from typing import Protocol, runtime_checkable

from funding_tracker.exchanges.dto import ContractInfo, FundingPoint


@runtime_checkable
class ExchangeAdapter(Protocol):
    """Contract for exchange API adapters.

    Adapters are modules (not classes) implementing this interface.
    LiveCollector detects available methods via hasattr().
    """

    EXCHANGE_ID: str

    async def get_contracts(self) -> list[ContractInfo]: ...

    async def fetch_history_before(
        self, symbol: str, before_timestamp: datetime | None
    ) -> list[FundingPoint]:
        """Fetch funding points before timestamp (backward fetching).

        Returns points in chronological order (oldest first).
        May contain duplicates across calls - caller should handle deduplication.
        """
        ...

    async def fetch_history_after(
        self, symbol: str, after_timestamp: datetime
    ) -> list[FundingPoint]:
        """Fetch funding points after timestamp (forward fetching).

        Returns points in chronological order (oldest first).
        May contain duplicates across calls - caller should handle deduplication.
        """
        ...

    async def fetch_live_batch(self) -> dict[str, FundingPoint]:
        """[PREFERRED] Get all unsettled rates in one API call."""
        ...

    async def fetch_live(self, symbol: str) -> FundingPoint:
        """[FALLBACK] Get unsettled rate for single symbol."""
        ...
