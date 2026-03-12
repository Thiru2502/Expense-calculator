from categorizer import categorize_expense


def test_categorize_by_keyword_match():
    assert categorize_expense("Uber trip downtown") == "Transport"
    assert categorize_expense("Amazon order payment") == "Shopping"


def test_categorize_default_other():
    assert categorize_expense("Unknown Vendor") == "Other"
