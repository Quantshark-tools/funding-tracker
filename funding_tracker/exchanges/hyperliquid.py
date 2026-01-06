import logging
from datetime import datetime

from funding_tracker.exchanges.dto import ContractInfo, FundingPoint
from funding_tracker.infrastructure import http_client

logger = logging.getLogger(__name__)

EXCHANGE_ID = "hyperliquid"
API_ENDPOINT = "https://api.hyperliquid.xyz/info"

# HyperLiquid API returns max 500 records per request
# Funding interval is 1 hour, so 500 records = 500 hours
# Use 498 hours (500 - 2) as safety buffer
_MAX_FETCH_WINDOW_HOURS = 498


async def get_contracts() -> list[ContractInfo]:
    logger.debug(f"Fetching contracts from {EXCHANGE_ID}")

    response = await http_client.post(
        API_ENDPOINT,
        json={"type": "meta"},
        headers={"Content-Type": "application/json"},
    )

    assert isinstance(response, dict)

    contracts = []
    for listing in response["universe"]:
        asset_name = listing["name"]
        contracts.append(
            ContractInfo(
                asset_name=asset_name,
                quote="USD",
                funding_interval=1,  # hourly funding
                section_name=EXCHANGE_ID,
            )
        )

    logger.debug(f"Fetched {len(contracts)} contracts from {EXCHANGE_ID}")
    return contracts


async def _fetch_history(symbol: str, start_time_ms: int, end_time_ms: int) -> list[FundingPoint]:
    logger.debug(
        f"Fetching history for {EXCHANGE_ID}/{symbol} "
        f"from {datetime.fromtimestamp(start_time_ms / 1000)} "
        f"to {datetime.fromtimestamp(end_time_ms / 1000)}"
    )

    response = await http_client.post(
        API_ENDPOINT,
        json={
            "type": "fundingHistory",
            "coin": symbol,
            "startTime": start_time_ms,
            "endTime": end_time_ms,
        },
        headers={"Content-Type": "application/json"},
    )

    points = []
    if response:
        assert isinstance(response, list)
        for raw_record in response:
            rate = float(raw_record["fundingRate"])
            timestamp = datetime.fromtimestamp(raw_record["time"] / 1000.0)
            points.append(FundingPoint(rate=rate, timestamp=timestamp))

    logger.debug(f"Fetched {len(points)} funding points for {EXCHANGE_ID}/{symbol}")
    return points


async def fetch_history_before(
    symbol: str, before_timestamp: datetime | None
) -> list[FundingPoint]:
    end_time_ms = int(
        (before_timestamp.timestamp() if before_timestamp else datetime.now().timestamp()) * 1000
    )
    start_time_ms = end_time_ms - (_MAX_FETCH_WINDOW_HOURS * 60 * 60 * 1000)

    logger.debug(
        f"Fetching backward history for {EXCHANGE_ID}/{symbol} before {before_timestamp or 'now'}"
    )

    return await _fetch_history(symbol, start_time_ms, end_time_ms)


async def fetch_history_after(symbol: str, after_timestamp: datetime) -> list[FundingPoint]:
    start_time_ms = int(after_timestamp.timestamp() * 1000)
    end_time_ms = int(datetime.now().timestamp() * 1000)

    logger.debug(f"Fetching forward history for {EXCHANGE_ID}/{symbol} after {after_timestamp}")

    return await _fetch_history(symbol, start_time_ms, end_time_ms)


async def fetch_live_batch() -> dict[str, FundingPoint]:
    logger.debug(f"Fetching live rates batch from {EXCHANGE_ID}")

    response = await http_client.post(
        API_ENDPOINT,
        json={"type": "metaAndAssetCtxs"},
        headers={"Content-Type": "application/json"},
    )

    assert isinstance(response, list)
    meta_data = response[0]["universe"]
    asset_contexts = response[1]

    asset_names = {i: asset["name"] for i, asset in enumerate(meta_data)}

    now = datetime.now()
    rates = {}
    for idx, ctx in enumerate(asset_contexts):
        if "funding" in ctx:
            asset_name = asset_names[idx]
            rates[asset_name] = FundingPoint(
                rate=float(ctx["funding"]),
                timestamp=now,
            )

    logger.debug(f"Fetched {len(rates)} live rates from {EXCHANGE_ID}")
    return rates
