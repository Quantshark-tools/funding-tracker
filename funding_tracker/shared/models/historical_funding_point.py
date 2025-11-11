from sqlalchemy import Index, PrimaryKeyConstraint

from funding_tracker.shared.models.base import BaseFundingPoint


class HistoricalFundingPoint(BaseFundingPoint, table=True):
    """Historical settled funding rate data point."""

    __tablename__: str = "funding_rate_record"

    __table_args__ = (
        PrimaryKeyConstraint("contract_id", "timestamp"),
        Index("ix_funding_rate_record_contract_id_timestamp", "contract_id", "timestamp"),
        {
            "timescaledb_hypertable": {"time_column_name": "timestamp"},
        },
    )
