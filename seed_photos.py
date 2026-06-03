import sqlite3

conn = sqlite3.connect("germanypath.db")
cur = conn.cursor()

cur.execute("SELECT id, slug, category, country_slug FROM programs ORDER BY id")
programs = cur.fetchall()

PHOTOS = {
    ("de", "AUSBILDUNG"): [
        "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1621905251918-48416bd8575a?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&h=500&fit=crop&q=80",
    ],
    ("de", "FSJ"): [
        "https://images.unsplash.com/photo-1582213782179-e0d53f98f2ca?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800&h=500&fit=crop&q=80",
    ],
    ("de", "AU_PAIR"): [
        "https://images.unsplash.com/photo-1476703993599-0035a21b17a9?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=800&h=500&fit=crop&q=80",
    ],
    ("de", "STUDIUM"): [
        "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800&h=500&fit=crop&q=80",
    ],
    ("de", "ARBEIT"): [
        "https://images.unsplash.com/photo-1560179707-f14e90ef3623?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&h=500&fit=crop&q=80",
    ],
    ("de", "LANGUAGE"): [
        "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&h=500&fit=crop&q=80",
    ],
    ("de", "IMMIGRATION"): [
        "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&h=500&fit=crop&q=80",
    ],
    ("de", "VOLUNTEERING"): [
        "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1593113598332-cd288d649433?w=800&h=500&fit=crop&q=80",
    ],
    ("ca", "STUDIUM"): [
        "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1607013251379-e6eecfffe234?w=800&h=500&fit=crop&q=80",
    ],
    ("ca", "ARBEIT"): [
        "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=800&h=500&fit=crop&q=80",
    ],
    ("ca", "IMMIGRATION"): [
        "https://images.unsplash.com/photo-1530521954074-e64f6810b32d?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&h=500&fit=crop&q=80",
    ],
    ("ca", "LANGUAGE"): [
        "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=800&h=500&fit=crop&q=80",
    ],
    ("fr", "STUDIUM"): [
        "https://images.unsplash.com/photo-1499856871958-5b9357976b82?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800&h=500&fit=crop&q=80",
    ],
    ("fr", "INTERNSHIP"): [
        "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=800&h=500&fit=crop&q=80",
    ],
    ("fr", "LANGUAGE"): [
        "https://images.unsplash.com/photo-1549144511-f099e773c147?w=800&h=500&fit=crop&q=80",
    ],
    ("ch", "STUDIUM"): [
        "https://images.unsplash.com/photo-1527840740656-c0ac5b4aeadb?w=800&h=500&fit=crop&q=80",
    ],
    ("ch", "ARBEIT"): [
        "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&h=500&fit=crop&q=80",
    ],
    ("pl", "STUDIUM"): [
        "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=800&h=500&fit=crop&q=80",
    ],
    ("pl", "ARBEIT"): [
        "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&h=500&fit=crop&q=80",
    ],
    ("us", "STUDIUM"): [
        "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=800&h=500&fit=crop&q=80",
        "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800&h=500&fit=crop&q=80",
    ],
    ("us", "INTERNSHIP"): [
        "https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=800&h=500&fit=crop&q=80",
    ],
    ("no", "STUDIUM"): [
        "https://images.unsplash.com/photo-1527004013197-933b977e8bce?w=800&h=500&fit=crop&q=80",
    ],
    ("se", "STUDIUM"): [
        "https://images.unsplash.com/photo-1508193638397-1c4234db14d8?w=800&h=500&fit=crop&q=80",
    ],
    ("fi", "STUDIUM"): [
        "https://images.unsplash.com/photo-1532712938310-34cb3982ef74?w=800&h=500&fit=crop&q=80",
    ],
    ("cz", "STUDIUM"): [
        "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?w=800&h=500&fit=crop&q=80",
    ],
    ("be", "STUDIUM"): [
        "https://images.unsplash.com/photo-1519452575417-564c1401ecc0?w=800&h=500&fit=crop&q=80",
    ],
    ("at", "STUDIUM"): [
        "https://images.unsplash.com/photo-1516550893923-42d28e5677af?w=800&h=500&fit=crop&q=80",
    ],
    ("at", "AUSBILDUNG"): [
        "https://images.unsplash.com/photo-1565043666747-69f6646db940?w=800&h=500&fit=crop&q=80",
    ],
    ("cn", "STUDIUM"): [
        "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=800&h=500&fit=crop&q=80",
    ],
    ("tr", "STUDIUM"): [
        "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=800&h=500&fit=crop&q=80",
    ],
}

FALLBACK = {
    "STUDIUM":      "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800&h=500&fit=crop&q=80",
    "ARBEIT":       "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&h=500&fit=crop&q=80",
    "AUSBILDUNG":   "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=800&h=500&fit=crop&q=80",
    "AU_PAIR":      "https://images.unsplash.com/photo-1476703993599-0035a21b17a9?w=800&h=500&fit=crop&q=80",
    "INTERNSHIP":   "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=800&h=500&fit=crop&q=80",
    "VOLUNTEERING": "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800&h=500&fit=crop&q=80",
    "FSJ":          "https://images.unsplash.com/photo-1582213782179-e0d53f98f2ca?w=800&h=500&fit=crop&q=80",
    "IMMIGRATION":  "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&h=500&fit=crop&q=80",
    "SCHULE":       "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800&h=500&fit=crop&q=80",
    "LANGUAGE":     "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800&h=500&fit=crop&q=80",
}

counters = {}
updated = 0

for prog_id, slug, category, country_slug in programs:
    cat = (category or "").upper()
    country = (country_slug or "").lower()
    key = (country, cat)
    photos = PHOTOS.get(key, [FALLBACK.get(cat, FALLBACK["STUDIUM"])])
    idx = counters.get(key, 0) % len(photos)
    counters[key] = idx + 1
    url = photos[idx]
    cur.execute("UPDATE programs SET cover_image_url = ? WHERE id = ?", (url, prog_id))
    updated += 1

conn.commit()
print(f"Updated {updated} programs with real photos")
conn.close()
