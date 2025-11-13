"""Coordinators for orchestrating exchange data collection.

This module provides universal coordinators that work with any exchange adapter:
- contract_syncer: Synchronize contract list from exchange to database
- history_fetcher: Fetch and store historical funding data
- live_collector: Collect current unsettled funding rates
- symbol_assembler: Convert Contract objects to exchange-specific symbols
"""

from funding_tracker.coordinators.contract_registry import register_contracts
from funding_tracker.coordinators.history_fetcher import sync_contract, update_contract
from funding_tracker.coordinators.live_collector import collect_live
from funding_tracker.coordinators.symbol_assembler import (
    SYMBOL_FORMATS,
    assemble_symbol,
)

__all__ = [
    "register_contracts",
    "sync_contract",
    "update_contract",
    "collect_live",
    "assemble_symbol",
    "SYMBOL_FORMATS",
]
