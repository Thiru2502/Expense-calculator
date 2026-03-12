# Expense Statement Categorizer

A Flask web app that accepts an uploaded account statement PDF, parses transactions, and groups expenses into categories.

## Features
- Upload a PDF statement from the browser.
- Parse transaction lines in the format: `DD/MM/YYYY Description 123.45`.
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

## Notes on PDF format
The parser expects transaction lines to resemble:

```text
01/02/2024 Grocery Store 54.23
05/02/2024 Uber Ride 14.50
```

If your bank uses a very different layout, adjust `parser.py` regex patterns.
