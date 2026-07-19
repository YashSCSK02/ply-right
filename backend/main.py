"""Entry point: run the ShopSphere enquiry flow and store results as JSON."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import config
from shop import EnquiryRecord, run


def save(records: list[EnquiryRecord], path: Path) -> None:
    payload = {
        "source": config.HOME_URL,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(records),
        "submitted": sum(1 for r in records if r.submitted),
        "enquiries": [r.to_dict() for r in records],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    records = run(config.TARGET_PRODUCTS, config.ENQUIRY_DETAILS)

    output = Path(__file__).parent / config.OUTPUT_FILE
    save(records, output)

    for record in records:
        status = "ok" if record.submitted else f"FAILED ({record.error})"
        print(f"{record.product.title}: {status}")
    print(f"\nWrote {len(records)} enquiries to {output}")


if __name__ == "__main__":
    main()
