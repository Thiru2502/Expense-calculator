from __future__ import annotations

import re
from dataclasses import dataclass
from io import BytesIO
from typing import Iterable

import pdfplumber


@dataclass(frozen=True)
class ParsedTransaction:
    date: str
    description: str
    amount: float


DATE_PATTERN = r"(?:\d{2}[/-]\d{2}[/-]\d{2,4})"
AMOUNT_PATTERN = r"\(?-?\d{1,3}(?:,\d{3})*(?:\.\d{2})\)?"
LINE_PATTERN = re.compile(
    rf"^(?P<date>{DATE_PATTERN})\s+(?P<description>.+?)\s+(?P<amount>{AMOUNT_PATTERN})(?:\s+(?P<balance>{AMOUNT_PATTERN}))?$"
)
IGNORE_IN_DESCRIPTION = (
    "opening balance",
    "closing balance",
    "available balance",
    "total",
    "withdrawal",
    "deposit",
)


def _parse_amount(amount_text: str) -> float:
    cleaned = amount_text.strip().replace(",", "")
    if cleaned.startswith("(") and cleaned.endswith(")"):
        cleaned = f"-{cleaned[1:-1]}"
    return float(cleaned)


def _description_looks_like_summary(description: str) -> bool:
    normalized = description.lower()
    return any(marker in normalized for marker in IGNORE_IN_DESCRIPTION)


def _lines_from_page(page: pdfplumber.page.Page) -> Iterable[str]:
    text = page.extract_text() or ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            yield stripped


def parse_statement_pdf(pdf_bytes: bytes) -> list[ParsedTransaction]:
    transactions: list[ParsedTransaction] = []

    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            for line in _lines_from_page(page):
                match = LINE_PATTERN.match(line)
                if not match:
                    continue

                description = match.group("description").strip("- ")
                if _description_looks_like_summary(description):
                    continue

                amount = _parse_amount(match.group("amount"))
                if amount <= 0:
                    continue

                transactions.append(
                    ParsedTransaction(
                        date=match.group("date"),
                        description=description,
                        amount=amount,
                    )
                )

    return transactions
