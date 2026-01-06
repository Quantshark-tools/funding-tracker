import logging
from datetime import datetime

from funding_tracker.exchanges.dto import ContractInfo, FundingPoint

logger = logging.getLogger(__name__)

# TODO: REPLACE WITH EXCHANGE_ID (e.g., "binance", "bybit", "okx")
EXCHANGE_ID = "TODO_EXCHANGE_ID"

# TODO: REPLACE WITH API BASE URL
API_ENDPOINT = "TODO_API_ENDPOINT"


async def get_contracts() -> list[ContractInfo]:
    # TODO: Fetch all perpetual contracts from exchange API
    # Return list of ContractInfo objects with asset_name, quote, funding_interval, section_name
    pass


async def fetch_history_before(
    symbol: str, before_timestamp: datetime | None
) -> list[FundingPoint]:
    # TODO: Fetch historical funding points before given timestamp (backward sync)
    # If before_timestamp is None, fetch from beginning
    # Return list of FundingPoint objects in chronological order
    pass


async def fetch_history_after(symbol: str, after_timestamp: datetime) -> list[FundingPoint]:
    # TODO: Fetch historical funding points after given timestamp (forward sync)
    # Return list of FundingPoint objects in chronological order
    pass


# TODO: IMPLEMENT ONE OF THE FOLLOWING (delete the other)


# Option A: Batch API (preferred) - fetch all symbols at once
async def fetch_live_batch() -> dict[str, FundingPoint]:
    # TODO: Fetch current funding rates for all symbols in one API call
    # Return dict mapping symbol → FundingPoint
    pass


# Option B: Individual API (fallback) - fetch one symbol at a time
# async def fetch_live(symbol: str) -> FundingPoint:
#     # TODO: Fetch current funding rate for single symbol
#     # Return FundingPoint or raise exception if not available
#     pass
