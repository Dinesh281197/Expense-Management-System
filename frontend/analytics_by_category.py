from datetime import datetime
import requests
import streamlit as st
import pandas as pd


API_URL =   " http://127.0.0.1:8000"

def analysis_by_category_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date:", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date:", datetime(2024, 8, 5))


    if st.button("Get Analytics"):
        payload = {
            "start_date" : start_date.strftime("%Y-%m-%d"),
            "end_date" : end_date.strftime("%Y-%m-%d")
        }
        response = requests.post(f"{API_URL}/analytics", json=payload)
        response_data = response.json()

        data = {
                "Category" : list(response_data.keys()),
                "Total(₹)" : [response_data[category]["total_amount"] for category in response_data],
                "Percentage" : [response_data[category]["percentage"] for category in response_data]
            }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values('Percentage', ascending=False)
        df_sorted['Total(₹)'] = df['Total(₹)'].map('{:.2f}'.format)
        df_sorted['Percentage'] = df['Percentage'].map('{:.0f}'.format).astype(str) + '%'
        st.title("Expense breakdown by  Category")
        st.bar_chart(data= df.set_index("Category")['Percentage'])
        df_sorted.set_index('Category', inplace=True)
        st.table(df_sorted)





