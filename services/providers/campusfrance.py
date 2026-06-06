"""
Campus France provider — PLACEHOLDER.

Status: NOT IMPLEMENTED (placeholder stub)

Why: Campus France does not provide a free public API for their
program database. Their search portal (campusfrance.org) is web-only.

To implement real integration:
  1. Contact Campus France: https://www.campusfrance.org/en
  2. Apply for data partnership or institutional access
  3. Check if they have an open data initiative

Official portal: https://www.campusfrance.org/en/course-catalog
"""
from typing import List, Optional

from services.providers.base import DataProvider, ProgramSyncDTO


class CampusFranceProvider(DataProvider):
    source_name = "campusfrance"

    async def fetch_programs(self) -> List[ProgramSyncDTO]:
        # Placeholder — returns empty list until real API access is configured
        return []

    async def fetch_program_detail(self, external_id: str) -> Optional[ProgramSyncDTO]:
        # Placeholder
        return None

    def is_configured(self) -> bool:
        return False
