from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from funding_tracker.shared.models.base import NameModel

if TYPE_CHECKING:
    from funding_tracker.shared.models.contract import Contract


class Asset(NameModel, table=True):
    market_cap_rank: int | None = Field(default=None, index=True)

    contracts: list["Contract"] = Relationship(
        back_populates="asset",
        sa_relationship_kwargs={
            "lazy": "selectin",
        },
    )
