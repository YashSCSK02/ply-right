# ShopSphere Playwright Automation

A Python Playwright automation project that interacts with the ShopSphere React application, submits product enquiries, stores scraped results in JSON, and persists successful enquiry records to PostgreSQL.

## Project Structure

```text
ply-right/
│
├── backend/
│   ├── config.py
│   ├── db.py
│   ├── main.py
│   ├── schema.sql
│   ├── shop.py
│   └── enquiries.json
│
├── .env
├── .gitignore
├── README.md
└── .venv/
```

## Prerequisites

Make sure the following are installed:

- Python 3
- PostgreSQL
- Git

## 1. Clone the Repository

```bash
git clone <repository-url>
cd ply-right
```

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

Install the required Python packages:

```bash
pip install playwright python-dotenv "psycopg[binary]"
```

Install the Playwright Chromium browser:

```bash
playwright install chromium
```

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```text
ply-right/
├── backend/
├── .env
└── README.md
```

Add the following configuration:

```env
# Target application
SHOP_BASE_URL="https://your-application-url.com"

# Login credentials
SHOP_EMAIL="test@example.com"
SHOP_PASSWORD="Password123"

# Enquiry details
SHOP_ENQUIRY_NAME="Test User"
SHOP_ENQUIRY_EMAIL="test.user@example.com"
SHOP_ENQUIRY_PHONE="9876543210"

# Browser configuration
SHOP_HEADLESS="false"
SHOP_SLOWMO="500"
SHOP_TIMEOUT_MS="30000"

# Output
SHOP_OUTPUT="enquiries.json"

# PostgreSQL
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="scrapper_db"
DB_USER="postgres"
DB_PASSWORD="your-password"
DB_SSLMODE="disable"
```

Do not commit the `.env` file to Git.

## 5. Create the PostgreSQL Database

Create the database:

```sql
CREATE DATABASE scrapper_db;
```

Connect to `scrapper_db` and run the SQL from:

```text
backend/schema.sql
```

The required table is:

```sql
CREATE TABLE enquiries (
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
    inserted_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_enquiries_product
ON enquiries (product_title);

CREATE INDEX idx_enquiries_scraped_at
ON enquiries (scraped_at DESC);
```

## 6. Run the Automation

From the project root:

```powershell
.\.venv\Scripts\python.exe backend\main.py
```

Or, if the virtual environment is already activated:

```bash
python backend/main.py
```

The automation will:

1. Launch the target ShopSphere application.
2. Log in using the configured credentials.
3. Find the configured target products.
4. Open the enquiry form.
5. Submit enquiry details.
6. Scrape the product and enquiry information.
7. Write the results to `backend/enquiries.json`.
8. Save successful enquiries to PostgreSQL.

Example output:

```text
MacBook Air M4: ok
Sony WH-1000XM6: ok
Keychron K2 V2: ok

Wrote 3 enquiries to backend/enquiries.json
Saved 3 successful enquiries to database (ids: [1, 2, 3])
```

## Verify Database Records

Run:

```sql
SELECT *
FROM enquiries
ORDER BY inserted_at DESC;
```

## Run in Headless Mode

To run without displaying the browser window, update `.env`:

```env
SHOP_HEADLESS="true"
SHOP_SLOWMO="0"
```

## Test Database Connection

From the `backend` directory:

```powershell
..\.venv\Scripts\python.exe -c "import db; conn=db.connect(); print('Connected to:', conn.info.dbname); conn.close()"
```

Expected output:

```text
Connected to: scrapper_db
```

## Load Existing JSON into PostgreSQL

If `backend/enquiries.json` already contains enquiry records, run from the `backend` directory:

```powershell
..\.venv\Scripts\python.exe db.py
```

## Notes

- Environment-specific configuration is managed through `.env`.
- Database credentials should never be committed to Git.
- The PostgreSQL database must be running before executing the automation.
- The target application must be accessible through `SHOP_BASE_URL`.
- Playwright browser binaries must be installed before the first run.
