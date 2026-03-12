from __future__ import annotations

import re
from dataclasses import dataclass
from io import BytesIO

import pdfplumber


@dataclass
class ParsedTransaction:
    date: str
    description: str
    amount: float


DATE_PATTERN = r"(?:\d{2}[/-]\d{2}[/-]\d{2,4})"
AMOUNT_PATTERN = r"-?\d{1,3}(?:,\d{3})*(?:\.\d{2})"
LINE_PATTERN = re.compile(
    rf"^(?P<date>{DATE_PATTERN})\s+(?P<description>.+?)\s+(?P<amount>{AMOUNT_PATTERN})$"
)


def parse_statement_pdf(pdf_bytes: bytes) -> list[ParsedTransaction]:
    extracted_lines: list[str] = []

    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            lines = [line.strip() for line in page_text.splitlines() if line.strip()]
            extracted_lines.extend(lines)

    transactions: list[ParsedTransaction] = []
    for line in extracted_lines:
        match = LINE_PATTERN.match(line)
        if not match:
            continue

        amount = float(match.group("amount").replace(",", ""))
        if amount <= 0:
            continue

        transactions.append(
            ParsedTransaction(
                date=match.group("date"),
                description=match.group("description"),
                amount=amount,
            )
        )

    return transactions
