from funding_tracker.shared.models.quote import Quote
from funding_tracker.shared.repositories.base import Repository


class QuoteRepository(Repository[Quote]):
    """Repository for managing quote currencies."""

    _model = Quote
