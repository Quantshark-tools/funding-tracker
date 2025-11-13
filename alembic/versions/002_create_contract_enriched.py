"""create_contract_enriched

Revision ID: 002
Revises: 001
Create Date: 2025-11-13 16:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: str | Sequence[str] | None = "001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create contract_enriched materialized view with helper function."""
    # Create helper function for funding multipliers
    op.execute("""
        CREATE OR REPLACE FUNCTION get_funding_multiplier(funding_interval INTEGER,
               target_hours NUMERIC)
        RETURNS NUMERIC AS $$
        BEGIN
            RETURN CASE funding_interval
                WHEN 1 THEN target_hours
                WHEN 2 THEN target_hours / 2.0
                WHEN 4 THEN target_hours / 4.0
                WHEN 8 THEN target_hours / 8.0
                ELSE target_hours / funding_interval
            END;
        END;
        $$ LANGUAGE plpgsql IMMUTABLE;
    """)

    # Create materialized view
    op.execute("""
        CREATE MATERIALIZED VIEW contract_enriched AS
        SELECT
            c.id,
            c.asset_name,
            c.quote_name,
            c.funding_interval,
            s.name as section_name,
            c.deprecated,
            -- Pre-computed multipliers for target intervals (1h, 8h, 1d, 365d)
            get_funding_multiplier(c.funding_interval, 1) as multiplier_1h,
            get_funding_multiplier(c.funding_interval, 8) as multiplier_8h,
            get_funding_multiplier(c.funding_interval, 24) as multiplier_1d,
            get_funding_multiplier(c.funding_interval, 8760) as multiplier_365d
        FROM contract c
        JOIN section s ON c.section_name = s.name
        WHERE c.deprecated = false;
    """)

    # Create UNIQUE index on id for CONCURRENTLY refresh
    op.execute("CREATE UNIQUE INDEX ON contract_enriched (id);")


def downgrade() -> None:
    """Drop contract_enriched materialized view and helper function."""
    # Drop materialized view
    op.execute("DROP MATERIALIZED VIEW IF EXISTS contract_enriched;")

    # Drop helper function
    op.execute("DROP FUNCTION IF EXISTS get_funding_multiplier(INTEGER, NUMERIC);")
