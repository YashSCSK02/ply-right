"""Postgres persistence for scraped enquiries.

The table this writes to is created by schema.sql.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

import psycopg

import config

INSERT_SQL = """
    INSERT INTO enquiries (
        product_title, brand, category, price, rating, stock,
        full_name, email, phone, submitted, error, scraped_at
    ) VALUES (
        %(product_title)s, %(brand)s, %(category)s, %(price)s, %(rating)s, %(stock)s,
        %(full_name)s, %(email)s, %(phone)s, %(submitted)s, %(error)s, %(scraped_at)s
    )
    RETURNING id
"""


def connect() -> psycopg.Connection:
    """Open a connection using the DB_* settings from .env."""
    return psycopg.connect(**config.DB)


def to_row(record: dict[str, Any]) -> dict[str, Any]:
    """Flatten one enquiry record into the columns the table expects."""
    product = record.get("product", {})
    details = record.get("details", {})
    return {
        "product_title": product.get("title"),
        "brand": product.get("brand"),
        "category": product.get("category"),
        "price": product.get("price"),
        "rating": product.get("rating"),
        "stock": product.get("stock"),
        "full_name": details.get("full_name"),
        "email": details.get("email"),
        "phone": details.get("phone"),
        "submitted": record.get("submitted", False),
        "error": record.get("error"),
        "scraped_at": record.get("timestamp"),
    }


def insert_enquiry(conn: psycopg.Connection, record: dict[str, Any]) -> int:
    """Insert a single enquiry and return its new id."""
    with conn.cursor() as cur:
        cur.execute(INSERT_SQL, to_row(record))
        return cur.fetchone()[0]


def insert_many(records: Iterable[dict[str, Any]]) -> list[int]:
    """Insert every record in one transaction; nothing is saved if any row fails."""
    with connect() as conn:
        ids = [insert_enquiry(conn, record) for record in records]
        conn.commit()
        return ids


def load_json(path: Path | str | None = None) -> list[int]:
    """Read an enquiries JSON file and insert everything it contains."""
    path = Path(path) if path else Path(__file__).parent / config.OUTPUT_FILE
    payload = json.loads(path.read_text(encoding="utf-8"))
    return insert_many(payload["enquiries"])


if __name__ == "__main__":
    import sys

    inserted = load_json(sys.argv[1] if len(sys.argv) > 1 else None)
    print(f"Inserted {len(inserted)} enquiries (ids: {inserted})")
