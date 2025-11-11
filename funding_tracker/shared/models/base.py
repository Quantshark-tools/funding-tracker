import datetime
import uuid

import sqlalchemy
from sqlmodel import Field, SQLModel


class UUIDModel(SQLModel, table=False):
    """Base model for entities with UUID primary key."""

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={"server_default": sqlalchemy.text("gen_random_uuid()"), "unique": True},
    )


class NameModel(SQLModel, table=False):
    """Base model for entities with string name as primary key."""

    name: str = Field(primary_key=True, index=True, unique=True)

    def __hash__(self) -> int:
        return hash(self.name)


class BaseFundingPoint(SQLModel, table=False):
    """Base model for funding rate data points."""

    timestamp: datetime.datetime
    contract_id: uuid.UUID = Field(foreign_key="contract.id")
    funding_rate: float

    def __hash__(self) -> int:
        return hash((self.contract_id, self.timestamp))
