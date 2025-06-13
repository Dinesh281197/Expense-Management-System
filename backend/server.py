from fastapi import  FastAPI, HTTPException
import db_helper
from datetime import date
from typing import List
from pydantic import BaseModel


class Expense(BaseModel):
    amount : float
    category : str
    notes : str

class DateRange(BaseModel):
    start_date : date
    end_date : date


app = FastAPI()


@app.get("/expenses/{expense_date}", response_model= List[Expense])
def get_expenses(expense_date : date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    return expenses


@app.post("/expenses/{expense_date}")
def view_add_or_update_expense(expense_date: date, expenses: List[Expense]):
    db_helper.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
    return {"message": "Expenses Updated Successfully"}



@app.post("/analytics")
def get_analytics(date_range: DateRange):
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=505, detail="Failed to retrieve the expense summary.")

    breakdown ={}
    total = sum([row['total_amount'] for row in data])
    for row in data:
        percentage = row['total_amount']/total*100 if total != 0 else 0
        breakdown[row['category']] = {"total_amount" : row['total_amount'],
                                      "percentage" : percentage}

    return breakdown


@app.get("/analytics/{year}")
def get_expenses_by_month(year:int):
    expenses_by_month = db_helper.fetch_expenses_by_month_for_year(year)
    if not expenses_by_month:
        raise HTTPException(status_code=404, detail="No expenses found for this year.")

    breakdown = {}
    total = sum([row['total_amount'] for row in expenses_by_month])
    for row in expenses_by_month:
        percentage = row['total_amount'] / total * 100 if total != 0 else 0
        breakdown[row['month_number']] = {"month_name":row["month_name"],"total_amount" : row["total_amount"],
                                   "percentage": percentage}
    return breakdown




