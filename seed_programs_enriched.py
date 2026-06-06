"""Enrich programs with cover images from Unsplash."""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./germanypath.db")

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(DATABASE_URL, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)

PROGRAM_IMAGES = {
    "de-fsj": "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800",
    "de-ausbildung": "https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=800",
    "de-au-pair": "https://images.unsplash.com/photo-1476703993599-0035a21b17a9?w=800",
    "de-study": "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=800",
    "de-chancenkarte": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800",
    "de-bfd": "https://images.unsplash.com/photo-1593113598332-cd288d649433?w=800",
    "fr-au-pair": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800",
    "fr-erasmus": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
    "fr-vie": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800",
    "fr-pvt": "https://images.unsplash.com/photo-1488085061387-422e29b40080?w=800",
    "fr-study-public": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800",
    "be-work": "https://images.unsplash.com/photo-1559113513-d5406b089b8b?w=800",
    "be-au-pair": "https://images.unsplash.com/photo-1476703993599-0035a21b17a9?w=800",
    "be-work-blue-card": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800",
    "be-study-kvb": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
    "ch-hotel-internship": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
    "ch-au-pair": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
    "ch-excellence-scholarship": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
    "ch-skilled-worker": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800",
    "at-ausbildung": "https://images.unsplash.com/photo-1516550893923-42d28e5677af?w=800",
    "at-red-white-red": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=800",
    "at-au-pair": "https://images.unsplash.com/photo-1476703993599-0035a21b17a9?w=800",
    "at-study": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800",
    "pl-work-visa": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800",
    "pl-study": "https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=800",
    "pl-it-internship": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800",
    "pl-seasonal-agri": "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=800",
    "cz-free-education": "https://images.unsplash.com/photo-1541849546-216549ae216d?w=800",
    "cz-au-pair": "https://images.unsplash.com/photo-1476703993599-0035a21b17a9?w=800",
    "cz-it-jobs": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800",
    "cz-erasmus": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
    "se-study": "https://images.unsplash.com/photo-1509356843151-3e7d96241e11?w=800",
    "se-si-scholarship": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
    "se-work-permit": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800",
    "se-berry-picking": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=800",
    "no-fish-industry": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800",
    "no-study": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=800",
    "no-skilled-worker": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800",
    "no-au-pair": "https://images.unsplash.com/photo-1476703993599-0035a21b17a9?w=800",
    "fi-berry-picking": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=800",
    "fi-study": "https://images.unsplash.com/photo-1538332576228-eb5b4c4de6f5?w=800",
    "fi-work-permit": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800",
    "fi-scholarship": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
    "tr-turkiye-burslari": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=800",
    "tr-internship": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
    "tr-language-school": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
    "tr-work-permit": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800",
    "cn-csc-scholarship": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800",
    "cn-teaching-english": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800",
    "cn-provincial-scholarship": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
    "cn-hsk-language": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
    "ca-express-entry": "https://images.unsplash.com/photo-1517935706615-2717063c2225?w=800",
    "ca-study-permit": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
    "ca-iec-working-holiday": "https://images.unsplash.com/photo-1488085061387-422e29b40080?w=800",
    "ca-pnp": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800",
    "us-work-travel": "https://images.unsplash.com/photo-1485738422979-f5c462d49f74?w=800",
    "us-au-pair": "https://images.unsplash.com/photo-1476703993599-0035a21b17a9?w=800",
    "us-j1-internship": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800",
    "us-fulbright": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
}


async def enrich():
    from models.program import Program

    async with Session() as db:
        updated = 0
        for slug, image_url in PROGRAM_IMAGES.items():
            result = await db.execute(select(Program).where(Program.slug == slug))
            program = result.scalar_one_or_none()
            if program and not program.cover_image_url:
                program.cover_image_url = image_url
                updated += 1
                print(f"[+] {slug}")
            elif program and program.cover_image_url:
                print(f"[~] {slug} already has image")
            else:
                print(f"[!] {slug} not found")

        await db.commit()
        print(f"\nEnriched {updated} programs.")


if __name__ == "__main__":
    asyncio.run(enrich())