from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CategoryRule:
    category: str
    keywords: tuple[str, ...]


RULES: tuple[CategoryRule, ...] = (
    CategoryRule("Groceries", ("grocery", "supermarket", "mart", "aldi", "walmart", "whole foods")),
    CategoryRule("Dining", ("restaurant", "cafe", "coffee", "uber eats", "doordash", "swiggy", "zomato")),
    CategoryRule("Transport", ("uber", "lyft", "taxi", "metro", "fuel", "petrol", "gas station")),
    CategoryRule("Utilities", ("electricity", "water", "internet", "broadband", "mobile", "phone bill")),
    CategoryRule("Rent", ("rent", "landlord", "property management")),
    CategoryRule("Entertainment", ("netflix", "spotify", "cinema", "movie", "games")),
    CategoryRule("Healthcare", ("pharmacy", "hospital", "clinic", "medical", "doctor")),
    CategoryRule("Shopping", ("amazon", "flipkart", "store", "mall", "ikea")),
)


def categorize_expense(description: str) -> str:
    normalized = description.lower()
    for rule in RULES:
        if any(keyword in normalized for keyword in rule.keywords):
            return rule.category
    return "Other"
