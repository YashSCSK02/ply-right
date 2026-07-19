"""Playwright automation for the ShopSphere demo store.

Logs in, opens the "View Details" enquiry modal for the configured products,
fills in the enquiry details and records everything to a JSON file.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, sync_playwright

import config


@dataclass
class Product:
    """Details scraped from a product card."""

    title: str
    brand: str | None = None
    category: str | None = None
    price: str | None = None
    rating: str | None = None
    stock: str | None = None


@dataclass
class EnquiryRecord:
    """One product enquiry, successful or not."""

    product: Product
    details: dict[str, str]
    submitted: bool
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _text_or_none(card, selector: str) -> str | None:
    """Return trimmed text for a child selector, or None if it is absent."""
    node = card.locator(selector)
    if node.count() == 0:
        return None
    return (node.first.inner_text() or "").strip() or None


def login(page: Page) -> None:
    """Authenticate and wait for the product catalogue to render."""
    page.goto(config.HOME_URL, wait_until="networkidle")
    page.fill("input[type='email']", config.LOGIN_EMAIL)
    page.fill("input[type='password']", config.LOGIN_PASSWORD)
    page.click("button[type='submit']")
    page.wait_for_selector("[data-testid='view-details']", timeout=config.TIMEOUT_MS)


def find_product_card(page: Page, title: str):
    """Locate the card whose title matches `title` exactly."""
    card = page.locator(
        "div.content", has=page.locator(f"[data-testid='product-title']:text-is('{title}')")
    )
    if card.count() == 0:
        raise LookupError(f"Product not found in catalogue: {title!r}")
    return card.first


def scrape_product(card) -> Product:
    """Read the visible attributes off a product card."""
    return Product(
        title=_text_or_none(card, "[data-testid='product-title']") or "",
        brand=_text_or_none(card, ".brand"),
        category=_text_or_none(card, "[data-testid='product-category']"),
        price=_text_or_none(card, "[data-testid='product-price']"),
        rating=_text_or_none(card, "[data-testid='product-rating']"),
        stock=_text_or_none(card, ".stock"),
    )


def fill_enquiry(page: Page, details: dict[str, str]) -> None:
    """Fill the enquiry modal. Assumes the modal is already open."""
    form = page.locator("form", has=page.locator("button:has-text('Submit Enquiry')")).first
    form.wait_for(state="visible", timeout=config.TIMEOUT_MS)

    form.locator("input[type='text']").fill(details["full_name"])
    form.locator("input[type='email']").fill(details["email"])
    form.locator("input[type='tel']").fill(details["phone"])


def submit_enquiry(page: Page) -> None:
    """Submit the modal and wait for it to close."""
    page.click("button:has-text('Submit Enquiry')")
    page.wait_for_selector(
        "button:has-text('Submit Enquiry')", state="hidden", timeout=config.TIMEOUT_MS
    )


def process_product(page: Page, title: str, details: dict[str, str]) -> EnquiryRecord:
    """Run the full enquiry flow for a single product."""
    card = find_product_card(page, title)
    product = scrape_product(card)

    try:
        card.locator("[data-testid='view-details']").click()
        fill_enquiry(page, details)
        submit_enquiry(page)
        return EnquiryRecord(product=product, details=details, submitted=True)
    except (PlaywrightTimeoutError, LookupError) as exc:
        # Leave the page usable for the next product.
        cancel = page.locator("button:has-text('Cancel')")
        if cancel.count() and cancel.first.is_visible():
            cancel.first.click()
        return EnquiryRecord(
            product=product, details=details, submitted=False, error=str(exc)
        )


def run(titles: list[str], details: dict[str, str]) -> list[EnquiryRecord]:
    """Log in once and process every requested product."""
    records: list[EnquiryRecord] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=config.HEADLESS, slow_mo=config.SLOW_MO_MS
        )
        page = browser.new_page()
        page.set_default_timeout(config.TIMEOUT_MS)

        try:
            login(page)
            for title in titles:
                try:
                    records.append(process_product(page, title, details))
                except LookupError as exc:
                    records.append(
                        EnquiryRecord(
                            product=Product(title=title),
                            details=details,
                            submitted=False,
                            error=str(exc),
                        )
                    )
        finally:
            browser.close()

    return records
