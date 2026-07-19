-- Run once against the target database:
--   psql -U postgres -h <db-host> -d scrapper_db -f schema.sql

CREATE TABLE IF NOT EXISTS enquiries (
    id            SERIAL PRIMARY KEY,
    product_title TEXT NOT NULL,
    brand         TEXT,
    category      TEXT,
    price         TEXT,
    rating        TEXT,
    stock         TEXT,
    full_name     TEXT NOT NULL,
    email         TEXT NOT NULL,
    phone         TEXT,
    submitted     BOOLEAN NOT NULL,
    error         TEXT,
    scraped_at    TIMESTAMPTZ NOT NULL,
    inserted_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_enquiries_product ON enquiries (product_title);
CREATE INDEX IF NOT EXISTS idx_enquiries_scraped_at ON enquiries (scraped_at DESC);
