from quantshark_shared.models.quote import Quote

from funding_tracker.db.repositories.base import Repository


class QuoteRepository(Repository[Quote]):
    """Repository for managing quote currencies."""

    _model = Quote
