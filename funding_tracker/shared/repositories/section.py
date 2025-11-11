from funding_tracker.shared.models.section import Section
from funding_tracker.shared.repositories.base import Repository


class SectionRepository(Repository[Section]):
    """Repository for managing exchange sections."""

    _model = Section
