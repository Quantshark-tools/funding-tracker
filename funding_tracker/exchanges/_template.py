# Template for creating new exchange adapter.
#
# INSTRUCTIONS:
# 1. Copy this file to exchanges/{exchange_name}.py (e.g., exchanges/binance.py)
# 2. Fill in all sections marked with TODO
# 3. Delete this comment block
# 4. Add your adapter to EXCHANGES registry in exchanges/__init__.py
# 5. Run tests to verify implementation
#
# This template implements the ExchangeAdapter protocol. See exchanges/protocol.py
# for detailed interface documentation.

import logging
from datetime import datetime

from funding_tracker.exchanges.dto import ContractInfo, FundingPoint
from funding_tracker.exchanges.utils import from_ms_timestamp, to_ms_timestamp
from funding_tracker.infrastructure import http_client

logger = logging.getLogger(__name__)

# =============================================================================
# STEP 1: Exchange Configuration
# =============================================================================

EXCHANGE_ID = "TODO_EXCHANGE_ID"  # Example: "binance", "bybit", "okx"
# Unique identifier for this exchange. Use lowercase, no spaces.

API_ENDPOINT = "TODO_API_ENDPOINT"  # Example: "https://api.binance.com"
# Base URL for the exchange's API.


# =============================================================================
# STEP 2: Implement get_contracts()
# =============================================================================

async def get_contracts() -> list[ContractInfo]:
    # TODO: Implementation steps:
    # 1. Find your exchange's API documentation for listing perpetual contracts
    # 2. Determine the HTTP method (GET or POST) and endpoint path
    # 3. Call the API using http_client.get() or http_client.post()
    # 4. Parse the response JSON
    # 5. Extract: asset name, quote currency, funding interval
    # 6. Return list of ContractInfo objects
    #
    # Example (HyperLiquid):
    #   response = await http_client.post(
    #       "https://api.hyperliquid.xyz/info",
    #       json={"type": "meta"},
    #       headers={"Content-Type": "application/json"},
    #   )
    #   # Response structure: {"universe": [{"name": "BTC"}, {"name": "ETH"}, ...]}
    #   contracts = []
    #   for listing in response["universe"]:
    #       asset_name = listing["name"]
    #       contracts.append(
    #           ContractInfo(
    #               asset_name=asset_name,
    #               quote="USD",
    #               funding_interval=1,  # hourly funding
    #               section_name=EXCHANGE_ID,
    #           )
    #       )
    #   return contracts

    logger.debug(f"Fetching contracts from {EXCHANGE_ID}")

    # TODO: Make API call to get contracts list
    response = await http_client.get(
        f"{API_ENDPOINT}/TODO_PATH",  # Example: "/v1/perpetual/contracts"
        params={"TODO": "TODO"},  # Add query parameters if needed
    )

    # TODO: Parse response into ContractInfo objects
    contracts = []
    for item in response["TODO_CONTRACTS_FIELD"]:  # Example: response["data"]
        contracts.append(
            ContractInfo(
                asset_name=item["TODO_ASSET_FIELD"],  # Example: item["symbol"]
                quote="TODO_QUOTE",  # Example: "USD" or "USDT"
                funding_interval=0,  # TODO: 1=hourly, 8=every 8 hours, etc.
                section_name=EXCHANGE_ID,
            )
        )

    logger.info(f"Fetched {len(contracts)} contracts from {EXCHANGE_ID}")
    return contracts


# =============================================================================
# STEP 3: Implement fetch_history()
# =============================================================================

async def fetch_history(
    symbol: str, after_timestamp: datetime | None
) -> list[FundingPoint]:
    # TODO: Implementation steps:
    # 1. Find your exchange's API documentation for historical funding rates
    # 2. Determine how to specify the symbol parameter
    # 3. Convert after_timestamp to exchange's format (ms, seconds, ISO string, etc.)
    # 4. Call the API using http_client.get() or http_client.post()
    # 5. Parse the response JSON
    # 6. Convert timestamps back to datetime objects
    # 7. Return list of FundingPoint objects
    #
    # Example (HyperLiquid):
    #   # HyperLiquid uses milliseconds for timestamps
    #   start_time_ms = int(after_timestamp.timestamp() * 1000) if after_timestamp else 0
    #   end_time_ms = int(datetime.now().timestamp() * 1000)
    #
    #   response = await http_client.post(
    #       "https://api.hyperliquid.xyz/info",
    #       json={
    #           "type": "fundingHistory",
    #           "coin": symbol,
    #           "startTime": start_time_ms,
    #           "endTime": end_time_ms,
    #       },
    #   )
    #   # Response: [{"fundingRate": "0.0001", "time": 1704067200000}, ...]
    #
    #   points = []
    #   if response:
    #       for record in response:
    #           rate = float(record["fundingRate"])
    #           timestamp = datetime.fromtimestamp(record["time"] / 1000.0)
    #           points.append(FundingPoint(rate=rate, timestamp=timestamp))
    #   return points
    #
    # Tip: Use utils.to_ms_timestamp() and utils.from_ms_timestamp() helpers!

    logger.debug(
        f"Fetching history for {EXCHANGE_ID}/{symbol} "
        f"from {after_timestamp or 'beginning'} to now"
    )

    # TODO: Convert timestamp to exchange format
    # Common formats:
    # - Milliseconds: to_ms_timestamp(after_timestamp)
    # - Seconds: int(after_timestamp.timestamp()) if after_timestamp else 0
    # - ISO string: after_timestamp.isoformat() if after_timestamp else None
    start_time = to_ms_timestamp(after_timestamp)  # TODO: Adjust for your exchange
    end_time = to_ms_timestamp(datetime.now())  # TODO: Some exchanges don't need this

    # TODO: Make API call to get funding history
    response = await http_client.get(
        f"{API_ENDPOINT}/TODO_PATH",  # Example: "/v1/funding/history"
        params={
            "symbol": symbol,  # TODO: Adjust parameter name
            "startTime": start_time,  # TODO: Adjust parameter names
            "endTime": end_time,  # TODO: Some exchanges don't need endTime
        },
    )

    # TODO: Parse response into FundingPoint objects
    points = []
    if response:  # Handle empty response
        for record in response["TODO_DATA_FIELD"]:  # Example: response["data"]
            rate = float(record["TODO_RATE_FIELD"])  # Example: record["fundingRate"]
            # TODO: Convert timestamp back to datetime
            # Common: from_ms_timestamp(record["timestamp"]) or
            #         datetime.fromtimestamp(record["timestamp"])
            timestamp = from_ms_timestamp(record["TODO_TIME_FIELD"])
            points.append(FundingPoint(rate=rate, timestamp=timestamp))

    logger.debug(f"Fetched {len(points)} funding points for {EXCHANGE_ID}/{symbol}")
    return points


# =============================================================================
# STEP 4: Implement live rate method(s)
# =============================================================================
#
# Choose ONE of the following options:
#
# Option A (PREFERRED): Batch API - if your exchange can return all symbols at once
# Option B (FALLBACK): Individual API - if you need to query one symbol at a time
#
# You only need to implement ONE option. Delete the other.
# =============================================================================


# -----------------------------------------------------------------------------
# Option A: Batch API (PREFERRED)
# -----------------------------------------------------------------------------
# Use this if your exchange has an endpoint like "get all tickers" or
# "get all perpetual stats" that returns data for ALL symbols in one call.
#
# Examples: HyperLiquid, Bybit, OKX have batch endpoints
# -----------------------------------------------------------------------------

async def fetch_live_batch() -> dict[str, FundingPoint]:
    # TODO: Implementation steps:
    # 1. Find your exchange's API endpoint that returns ALL symbols' data
    # 2. Call the API using http_client.get() or http_client.post()
    # 3. Parse the response JSON
    # 4. Build a dict mapping symbol → FundingPoint
    # 5. Return the dict
    #
    # Example (HyperLiquid):
    #   response = await http_client.post(
    #       "https://api.hyperliquid.xyz/info",
    #       json={"type": "metaAndAssetCtxs"},
    #   )
    #   # Response: [meta_data, asset_contexts]
    #   # meta_data["universe"] has asset names
    #   # asset_contexts has array of {"funding": "0.0001", ...}
    #
    #   meta_data = response[0]["universe"]
    #   asset_contexts = response[1]
    #
    #   asset_names = {i: asset["name"] for i, asset in enumerate(meta_data)}
    #
    #   now = datetime.now()
    #   rates = {}
    #   for idx, ctx in enumerate(asset_contexts):
    #       if "funding" in ctx:
    #           asset_name = asset_names[idx]
    #           rates[asset_name] = FundingPoint(
    #               rate=float(ctx["funding"]),
    #               timestamp=now,
    #           )
    #   return rates

    logger.debug(f"Fetching live rates batch from {EXCHANGE_ID}")

    # TODO: Make API call to get all symbols' data at once
    response = await http_client.get(
        f"{API_ENDPOINT}/TODO_PATH",  # Example: "/v1/ticker/all"
    )

    # TODO: Parse response into symbol → FundingPoint dict
    now = datetime.now()
    rates = {}
    for item in response["TODO_DATA_FIELD"]:
        symbol = item["TODO_SYMBOL_FIELD"]  # Example: item["symbol"]
        funding_rate = float(item["TODO_RATE_FIELD"])  # Example: item["fundingRate"]
        rates[symbol] = FundingPoint(rate=funding_rate, timestamp=now)

    logger.info(f"Fetched {len(rates)} live rates from {EXCHANGE_ID}")
    return rates


# -----------------------------------------------------------------------------
# Option B: Individual API (FALLBACK)
# -----------------------------------------------------------------------------
# Use this ONLY if your exchange doesn't have a batch endpoint.
# The coordinator will call this N times in parallel (with semaphore control).
#
# Note: If you implement fetch_live_batch(), DELETE this function.
# The coordinator will automatically detect and use the batch method.
# -----------------------------------------------------------------------------

# async def fetch_live(symbol: str) -> FundingPoint | None:
#     # TODO: Implementation steps:
#     # 1. Find your exchange's API endpoint for single symbol ticker/funding
#     # 2. Call the API using http_client.get() or http_client.post()
#     # 3. Parse the response JSON
#     # 4. Return FundingPoint or None if not available
#     #
#     # Example (hypothetical individual API):
#     #   response = await http_client.get(
#     #       f"{API_ENDPOINT}/v1/ticker/{symbol}",
#     #   )
#     #   if "fundingRate" not in response:
#     #       return None
#     #   return FundingPoint(
#     #       rate=float(response["fundingRate"]),
#     #       timestamp=datetime.now(),
#     #   )
#
#     logger.debug(f"Fetching live rate for {EXCHANGE_ID}/{symbol}")
#
#     # TODO: Make API call to get single symbol's data
#     response = await http_client.get(
#         f"{API_ENDPOINT}/TODO_PATH/{symbol}",  # Example: "/v1/ticker/{symbol}"
#     )
#
#     # TODO: Parse response
#     if "TODO_RATE_FIELD" not in response:
#         return None
#
#     return FundingPoint(
#         rate=float(response["TODO_RATE_FIELD"]),
#         timestamp=datetime.now(),
#     )


# =============================================================================
# FINAL STEP: Register your adapter
# =============================================================================
# After implementing this file:
# 1. Go to exchanges/__init__.py
# 2. Import your module: from funding_tracker.exchanges import your_exchange
# 3. Add to registry: EXCHANGES["your_exchange"] = your_exchange
# 4. The validation function will automatically check your implementation
# =============================================================================
