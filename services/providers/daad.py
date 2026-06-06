"""
DAAD (Deutscher Akademischer Austauschdienst) provider — PLACEHOLDER.

Status: NOT IMPLEMENTED (placeholder stub)

Why: DAAD does not provide a free public API for programmatic access to
their scholarship/program database. Their website (daad.de) uses internal
search APIs that require session cookies and are not publicly documented.

To implement real integration:
  1. Contact DAAD directly: https://www.daad.de/en/information-services-for-higher-education-institutions/
  2. Apply for institutional API access if available
  3. OR use the public scholarship search with proper web scraping consent

Official DAAD scholarship database: https://www.daad.de/de/studieren-und-forschen-in-deutschland/stipendien-finden/
"""
from typing import List, Optional

from services.providers.base import DataProvider, ProgramSyncDTO


class DAADProvider(DataProvider):
    source_name = "daad"

    async def fetch_programs(self) -> List[ProgramSyncDTO]:
        # Placeholder — returns empty list until real API access is configured
        return []

    async def fetch_program_detail(self, external_id: str) -> Optional[ProgramSyncDTO]:
        # Placeholder
        return None

    def is_configured(self) -> bool:
        return False
