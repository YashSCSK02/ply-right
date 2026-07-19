"""Entry point: run the ShopSphere enquiry flow and store results as JSON and DB."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import config
from shop import EnquiryRecord, run

try:
    import db
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False


def save(records: list[EnquiryRecord], path: Path) -> None:
    payload = {
        "source": config.HOME_URL,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(records),
        "submitted": sum(1 for r in records if r.submitted),
        "enquiries": [r.to_dict() for r in records],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def save_to_db(records: list[EnquiryRecord]) -> None:
    """Save successful enquiries (no errors) to the database."""
    if not DB_AVAILABLE:
        print("Warning: db module not available, skipping database save")
        return
    
    successful_records = [r for r in records if r.submitted and r.error is None]
    if not successful_records:
        print("No successful enquiries to save to database")
        return
    
    try:
        ids = db.insert_many([r.to_dict() for r in successful_records])
        print(f"Saved {len(ids)} successful enquiries to database (ids: {ids})")
    except Exception as e:
        print(f"Error saving to database: {e}")


def main() -> None:
    records = run(config.TARGET_PRODUCTS, config.ENQUIRY_DETAILS)

    output = Path(__file__).parent / config.OUTPUT_FILE
    save(records, output)

    for record in records:
        status = "ok" if record.submitted else f"FAILED ({record.error})"
        print(f"{record.product.title}: {status}")
    print(f"\nWrote {len(records)} enquiries to {output}")
    
    # Save successful enquiries to database
    save_to_db(records)


if __name__ == "__main__":
    main()
