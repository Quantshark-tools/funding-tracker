"""Thin application entrypoint for funding tracker."""

from __future__ import annotations

import asyncio
import logging
import os
import sys
import time

from dotenv import load_dotenv

from funding_tracker.bootstrap import bootstrap
from funding_tracker.cli import build_parser
from funding_tracker.exchanges import EXCHANGES
from funding_tracker.logging_setup import (
    configure_exchange_debug_logging,
    configure_live_debug_logging,
    configure_logging,
)
from funding_tracker.runtime import build_runtime_config
from funding_tracker.settings import Settings

logger = logging.getLogger(__name__)


def _force_utc_timezone() -> None:
    """Set process timezone to UTC before scheduler starts."""
    os.environ["TZ"] = "UTC"
    if hasattr(time, "tzset"):
        time.tzset()


async def run_scheduler(db_connection: str, exchanges: list[str] | None) -> None:
    """Bootstrap and run scheduler forever."""
    scheduler = await bootstrap(db_connection=db_connection, exchanges=exchanges)
    scheduler.start()
    logger.info("Scheduler started, waiting for jobs...")
    await asyncio.Event().wait()


def main() -> None:
    """Main entrypoint used by CLI and supervisord."""
    _force_utc_timezone()
    load_dotenv()

    args = build_parser().parse_args()

    try:
        settings = Settings()  # type: ignore[call-arg]
        config = build_runtime_config(args=args, settings=settings, all_exchanges=set(EXCHANGES))
    except Exception as exc:
        sys.exit(f"Configuration error: {exc}")

    configure_logging(instance_id=config.instance_id, total_instances=config.total_instances)
    configure_exchange_debug_logging(config.debug_exchanges)
    configure_live_debug_logging(config.debug_exchanges_live)

    if config.total_instances > 1:
        logger.info(
            "Instance %s/%s: running %s exchange(s): %s",
            config.instance_id,
            config.total_instances,
            len(config.exchanges or []),
            config.exchanges or [],
        )
    elif config.exchanges:
        logger.info(
            "Starting funding tracker with %s exchange(s): %s",
            len(config.exchanges),
            config.exchanges,
        )
    else:
        logger.info("Starting funding tracker with all exchanges")

    try:
        asyncio.run(run_scheduler(config.db_connection, config.exchanges))
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as exc:
        logger.error("Application error: %s", exc, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
