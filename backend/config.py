"""Configuration for the ShopSphere Playwright automation."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Required environment variable '{name}' is not set."
        )

    return value


BASE_URL = required_env("SHOP_BASE_URL")
HOME_URL = f"{BASE_URL.rstrip('/')}/home"

LOGIN_EMAIL = required_env("SHOP_EMAIL")
LOGIN_PASSWORD = required_env("SHOP_PASSWORD")

TARGET_PRODUCTS = [
    "MacBook Air M4",
    "Sony WH-1000XM6",
    "Keychron K2 V2",
]

ENQUIRY_DETAILS = {
    "full_name": required_env("SHOP_ENQUIRY_NAME"),
    "email": required_env("SHOP_ENQUIRY_EMAIL"),
    "phone": required_env("SHOP_ENQUIRY_PHONE"),
}

OUTPUT_FILE = os.getenv(
    "SHOP_OUTPUT",
    "enquiries.json",
)

DB = {
    "host": required_env("DB_HOST"),
    "port": int(required_env("DB_PORT")),
    "dbname": required_env("DB_NAME"),
    "user": required_env("DB_USER"),
    "password": required_env("DB_PASSWORD"),
    "sslmode": required_env("DB_SSLMODE"),
}

HEADLESS = (
    os.getenv("SHOP_HEADLESS", "true").lower()
    != "false"
)

SLOW_MO_MS = int(
    os.getenv("SHOP_SLOWMO", "0")
)

TIMEOUT_MS = int(
    os.getenv("SHOP_TIMEOUT_MS", "30000")
)