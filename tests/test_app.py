from io import BytesIO

import pytest

pytest.importorskip("flask")
import app as webapp


def test_index_renders_homepage():
    client = webapp.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Expense Statement Categorizer" in response.data


def test_post_requires_pdf_file():
    client = webapp.app.test_client()
    response = client.post(
        "/",
        data={"statement": (BytesIO(b"hello"), "statement.txt")},
        content_type="multipart/form-data",
    )
    assert b"Only PDF files are supported." in response.data


def test_post_shows_summary(monkeypatch):
    client = webapp.app.test_client()

    class Tx:
        def __init__(self, description, amount):
            self.description = description
            self.amount = amount

    monkeypatch.setattr(
        webapp,
        "parse_statement_pdf",
        lambda _pdf: [Tx("Uber ride", 20.0), Tx("Amazon order", 80.0)],
    )

    response = client.post(
        "/",
        data={"statement": (BytesIO(b"fake"), "statement.pdf")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"Transactions analyzed" in response.data
    assert b"Transport" in response.data
    assert b"Shopping" in response.data
