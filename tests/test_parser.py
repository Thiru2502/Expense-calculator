from types import SimpleNamespace

import pytest

pytest.importorskip("pdfplumber")
import parser


class FakePdf:
    def __init__(self, lines):
        self.pages = [SimpleNamespace(extract_text=lambda: "\n".join(lines))]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_parse_statement_pdf_filters_and_extracts(monkeypatch):
    lines = [
        "01/02/2024 Grocery Store 54.23",
        "02/02/2024 Salary 1000.00",
        "03-02-2024 Metro Card Reload 1,234.56 9,876.54",
        "04/02/2024 Utility Payment (45.00)",
        "05/02/2024 Opening Balance 999.99",
    ]
    monkeypatch.setattr(parser.pdfplumber, "open", lambda *_: FakePdf(lines))

    result = parser.parse_statement_pdf(b"fake-pdf")

    assert [tx.description for tx in result] == [
        "Grocery Store",
        "Salary",
        "Metro Card Reload",
    ]
    assert [tx.amount for tx in result] == [54.23, 1000.00, 1234.56]


def test_parse_amount_parentheses_negative():
    assert parser._parse_amount("(45.00)") == -45.0
