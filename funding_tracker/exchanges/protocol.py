"""Exchange adapter protocol.

Structural interface for exchange modules. Adapters implement required methods
without explicit inheritance. See exchanges/README.md for integration guide.
"""

from datetime import datetime
from typing import Protocol, runtime_checkable

from funding_tracker.exchanges.dto import ContractInfo, FundingPoint


@runtime_checkable
class ExchangeAdapter(Protocol):
    """Contract for exchange API adapters.

    Adapters are modules (not classes) implementing this interface.
    LiveCollector detects available methods via hasattr().

    Required: EXCHANGE_ID, get_contracts(), fetch_history()
    Optional: fetch_live_batch() [preferred] OR fetch_live()
    """

    EXCHANGE_ID: str

    async def get_contracts(self) -> list[ContractInfo]: ...

    async def fetch_history(
        self, symbol: str, after_timestamp: datetime | None
    ) -> list[FundingPoint]:
        """Returns funding points after timestamp; may contain duplicates."""
        ...

    async def fetch_live_batch(self) -> dict[str, FundingPoint]:
        """[OPTIONAL - PREFERRED] Get all unsettled rates in one API call."""
        ...

    async def fetch_live(self, symbol: str) -> FundingPoint:
        """[OPTIONAL - FALLBACK] Get unsettled rate for single symbol."""
        ...
