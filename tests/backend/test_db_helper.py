import pytest
from backend  import db_helper

def test_fetch_expenses_for_date():
    expenses = db_helper.fetch_expenses_for_date("2024-08-15")
    assert len(expenses) == 1

def test_fetch_expense_summary():
    expenses = db_helper.fetch_expense_summary("2024-08-15", "2024-08-29")
    assert len(expenses) == 6