from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship

from funding_tracker.shared.models.base import NameModel

if TYPE_CHECKING:
    from funding_tracker.shared.models.contract import Contract


class Section(NameModel, table=True):
    """Exchange or trading section (e.g., binance, bybit)."""

    special_fields: dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON, server_default="{}")
    )

    contracts: list["Contract"] = Relationship(
        back_populates="section",
        sa_relationship_kwargs={
            "lazy": "selectin",
        },
    )
