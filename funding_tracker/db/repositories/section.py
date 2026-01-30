from quantshark_shared.models.section import Section

from funding_tracker.db.repositories.base import Repository


class SectionRepository(Repository[Section]):
    """Repository for managing exchange sections."""

    _model = Section
