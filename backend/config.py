"""Configuration for the ShopSphere Playwright automation.

Settings come from the project-root .env file, overridden by any real
environment variables already set in the shell.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# .env lives at the project root, one level above backend/.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

BASE_URL = os.getenv("SHOP_BASE_URL", "https://react-test-shop-five.vercel.app")
HOME_URL = f"{BASE_URL}/home"

# The demo site accepts any well-formed credentials.
LOGIN_EMAIL = os.getenv("SHOP_EMAIL", "test@example.com")
LOGIN_PASSWORD = os.getenv("SHOP_PASSWORD", "Password123")

# Products to enquire about, matched on the card title (exact text).
TARGET_PRODUCTS = [
    "MacBook Air M4",
    "Sony WH-1000XM6",
    "Keychron K2 V2",
]

# Details typed into the "View Details" enquiry modal.
ENQUIRY_DETAILS = {
    "full_name": "Test User",
    "email": "test.user@example.com",
    "phone": "9876543210",  # site caps this input at 10 characters
}

OUTPUT_FILE = os.getenv("SHOP_OUTPUT", "enquiries.json")

# Postgres connection. DB_HOST is the machine running the database, which may
# not be this one.
DB = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "scrapper_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "sslmode": os.getenv("DB_SSLMODE", "prefer"),
}

HEADLESS = os.getenv("SHOP_HEADLESS", "true").lower() != "false"

# Milliseconds Playwright pauses between actions, so a visible run is followable.
SLOW_MO_MS = int(os.getenv("SHOP_SLOWMO", "0"))

TIMEOUT_MS = 30_000
