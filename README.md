# Expense Statement Categorizer

A Flask web app that accepts an uploaded account statement PDF, parses debit transactions, and groups expenses into categories.

## Features
- Upload a PDF statement from the browser.
- Parse transaction lines in flexible formats like:
  - `DD/MM/YYYY Description 123.45`
  - `DD-MM-YYYY Description 1,234.56 9,876.54` (with trailing balance)
  - `DD/MM/YYYY Description (45.00)` (parenthesis amount handling)
- Ignore non-expense lines such as balances and totals.
- Auto-categorize expenses using keyword-based rules.
- View category-wise totals and percentage share.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

## Notes
- This parser is regex-driven and works best with text-based PDFs (not scanned images).
- If your bank uses different statement text layouts, update patterns in `parser.py`.
