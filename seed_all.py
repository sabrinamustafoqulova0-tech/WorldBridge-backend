"""seed_all.py — Run all seed scripts in order."""
import asyncio
import logging
import sys
import os

os.environ.setdefault("PYTHONIOENCODING", "utf-8")
logging.basicConfig(level=logging.INFO)

async def main():
    from seed_countries import seed_countries
    from seed_programs_1 import seed_programs_1
    from seed_programs_2 import seed_programs_2
    from seed_programs_3 import seed_programs_3
    from seed_programs_4 import seed_programs_4
    from seed_faq import seed_faq

    print("\n[1/6] Seeding countries...")
    await seed_countries()

    print("\n[2/6] Seeding programs batch 1 (DE/FR/BE)...")
    await seed_programs_1()

    print("\n[3/6] Seeding programs batch 2 (CH/AT/PL/CZ/SE/NO/FI)...")
    await seed_programs_2()

    print("\n[4/6] Seeding programs batch 3 (TR/CN/CA/US)...")
    await seed_programs_3()

    print("\n[5/6] Seeding programs batch 4 (all countries, additional real programs)...")
    await seed_programs_4()

    print("\n[6/6] Seeding FAQs...")
    await seed_faq()

    print("\nAll data seeded successfully!")

if __name__ == "__main__":
    asyncio.run(main())
