import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logging

import os
from dotenv import load_dotenv

load_dotenv()

logger = setup_logging('db_helper')

@contextmanager
def get_db_cursor(do_commit = False):
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    if connection.is_connected():
        print('connected successful')
    else:
        print('connection failed')

    cursor = connection.cursor(dictionary = True)
    yield cursor

    if do_commit:
     connection.commit()

    cursor.close()
    connection.close()


def fetch_expense_summary(start_date, end_date):
    logger.info(f'fetch expense summary called with start: {start_date} end: {end_date}')
    with get_db_cursor() as cursor:
        cursor.execute(f"""select  category, sum(amount) as total_amount from expenses 
                                where expense_date between  %s and %s 
                                group by  category""",
                        (start_date,end_date))
        expense_summary = cursor.fetchall()
        return expense_summary



def fetch_expenses_for_date(expense_date):
    logger.info(f'fetch expenses for date with {expense_date}')
    with  get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses where expense_date = %s ",(expense_date,))
        expenses_for_date = cursor.fetchall()
        return expenses_for_date



def fetch_expenses_by_month_for_year(year):
    logger.info(f'fetch expenses by month for year with {year}')
    with  get_db_cursor() as cursor:
        cursor.execute(f"""select  MONTH(expense_date) as month_number ,monthname(expense_date) as month_name ,sum(amount) as total_amount from expenses 
                                    where year(expense_date) = %s
                                    group by  month_number , month_name""",
                            (year,))
        expenses_by_month  = cursor.fetchall()
        return expenses_by_month



def delete_expenses_for_date(expense_date):
    logger.info(f'delete expenses for date with {expense_date}')
    with get_db_cursor(do_commit = True) as cursor:
        cursor.execute("DELETE FROM expenses where expense_date = %s ", (expense_date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f'insert expense for date with {expense_date} and amount: {amount}, category: {category}, notes: {notes}')
    with get_db_cursor(do_commit = True) as cursor:
        cursor.execute("INSERT INTO expenses(expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
                       (expense_date, amount, category, notes))




# print("DB Host:", os.getenv("DB_HOST"))