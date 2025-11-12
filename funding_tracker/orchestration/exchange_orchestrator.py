"""Exchange orchestrator."""

import asyncio
import logging
from datetime import datetime
from typing import TYPE_CHECKING

from funding_tracker.coordinators.contract_registry import (
    MaterializedViewRefresher,
    register_contracts,
)
from funding_tracker.coordinators.history_fetcher import sync_contract, update_contract
from funding_tracker.coordinators.live_collector import collect_live
from funding_tracker.coordinators.symbol_assembler import assemble_symbol
from funding_tracker.shared.models.contract import Contract
from funding_tracker.unit_of_work import UOWFactoryType

if TYPE_CHECKING:
    from funding_tracker.exchanges.protocol import ExchangeAdapter

logger = logging.getLogger(__name__)


class ExchangeOrchestrator:
    """Coordinates update() and update_live() operations for scheduler."""

    def __init__(
        self,
        exchange_adapter: "ExchangeAdapter",
        section_name: str,
        uow_factory: UOWFactoryType,
        semaphore: asyncio.Semaphore,
        mv_refresher: MaterializedViewRefresher,
    ) -> None:
        self._exchange_adapter = exchange_adapter
        self._section_name = section_name
        self._uow_factory = uow_factory
        self._mv_refresher = mv_refresher
        self._semaphore = semaphore

    async def update(self) -> None:
        """Register contracts, then sync/update history for each."""
        start_time = datetime.now()
        logger.info(f"Starting update for {self._section_name}")

        try:
            await register_contracts(
                self._exchange_adapter,
                self._section_name,
                self._uow_factory,
                self._mv_refresher,
            )
        except Exception as e:
            logger.error(
                f"Failed to register contracts for {self._section_name}: {e}",
                exc_info=True,
            )
            return

        async with self._uow_factory() as uow:
            contracts = await uow.contracts.get_by_section(self._section_name)

        if not contracts:
            logger.warning(f"No contracts found for {self._section_name}")
            duration = datetime.now() - start_time
            logger.info(
                f"Update completed for {self._section_name} in {duration} "
                f"(no contracts to process)"
            )
            return

        logger.debug(f"Processing {len(contracts)} contracts for {self._section_name}")

        async def process_contract(contract: Contract) -> None:
            async with self._semaphore:
                try:
                    if not contract.synced:
                        await sync_contract(
                            self._exchange_adapter,
                            contract,
                            self._uow_factory,
                            assemble_symbol,
                        )
                    else:
                        await update_contract(
                            self._exchange_adapter,
                            contract,
                            self._uow_factory,
                            assemble_symbol,
                        )
                except Exception as e:
                    logger.error(
                        f"Failed to process contract {contract.asset.name}/{contract.quote_name} "
                        f"on {self._section_name}: {e}",
                        exc_info=True,
                    )

        tasks = [process_contract(contract) for contract in contracts]
        await asyncio.gather(*tasks)

        duration = datetime.now() - start_time
        logger.info(
            f"Update completed for {self._section_name} in {duration} "
            f"({len(contracts)} contracts processed)"
        )

    async def update_live(self) -> None:
        """Collect live funding rates for all active contracts."""
        logger.debug(f"Collecting live rates for {self._section_name}")

        try:
            await collect_live(
                self._exchange_adapter,
                self._section_name,
                self._uow_factory,
                assemble_symbol,
                self._semaphore,
            )
        except Exception as e:
            logger.error(
                f"Failed to collect live rates for {self._section_name}: {e}",
                exc_info=True,
            )
