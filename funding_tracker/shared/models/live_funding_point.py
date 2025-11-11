from sqlalchemy import PrimaryKeyConstraint

from funding_tracker.shared.models.base import BaseFundingPoint


class LiveFundingPoint(BaseFundingPoint, table=True):
    """Live unsettled funding rate data point."""

    __tablename__: str = "unsettled_funding_rate_record"

    __table_args__ = (
        PrimaryKeyConstraint("contract_id", "timestamp"),
        {
            "timescaledb_hypertable": {"time_column_name": "timestamp"},
        },
    )
