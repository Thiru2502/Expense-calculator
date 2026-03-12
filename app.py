from __future__ import annotations

from flask import Flask, render_template, request

from categorizer import categorize_expense
from parser import parse_statement_pdf

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB upload limit


@app.route("/", methods=["GET", "POST"])
def index():
    summary_rows = []
    total_expense = 0.0
    transaction_count = 0
    error = None

    if request.method == "POST":
        uploaded_file = request.files.get("statement")

        if not uploaded_file or uploaded_file.filename == "":
            error = "Please upload a PDF account statement."
        elif not uploaded_file.filename.lower().endswith(".pdf"):
            error = "Only PDF files are supported."
        else:
            try:
                transactions = parse_statement_pdf(uploaded_file.read())
            except Exception:
                error = "Could not read this PDF. Please try a text-based statement export."
                transactions = []

            if not error and not transactions:
                error = (
                    "No debit transactions could be parsed. Expected lines like "
                    "'DD/MM/YYYY Description 123.45'."
                )

            if not error:
                transaction_count = len(transactions)
                category_totals: dict[str, float] = {}
                for tx in transactions:
                    category = categorize_expense(tx.description)
                    category_totals[category] = category_totals.get(category, 0.0) + tx.amount

                total_expense = sum(category_totals.values())
                summary_rows = sorted(
                    (
                        {
                            "category": category,
                            "amount": amount,
                            "percent": (amount / total_expense) * 100 if total_expense else 0,
                        }
                        for category, amount in category_totals.items()
                    ),
                    key=lambda row: row["amount"],
                    reverse=True,
                )

    return render_template(
        "index.html",
        summary_rows=summary_rows,
        total_expense=total_expense,
        transaction_count=transaction_count,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
