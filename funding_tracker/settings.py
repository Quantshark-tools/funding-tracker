"""Environment-backed settings for funding tracker."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment and .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    db_connection: str = Field(alias="DB_CONNECTION")
    debug_exchanges: str | None = Field(default=None, alias="DEBUG_EXCHANGES")
    debug_exchanges_live: str | None = Field(default=None, alias="DEBUG_EXCHANGES_LIVE")
    exchanges: str | None = Field(default=None, alias="EXCHANGES")
    instance_id: int = Field(default=0, alias="INSTANCE_ID")
    total_instances: int = Field(default=1, alias="TOTAL_INSTANCES")
