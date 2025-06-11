import requests
import streamlit as st
import pandas as pd

API_URL =   "http://127.0.0.1:8000"

def analysis_by_month_tab():
    years = list(range(2000, 2031))
    selected_year = st.selectbox(label = "Select Year", options=years, index=years.index(2024))

    if selected_year:
        response = requests.get(f"{API_URL}/analytics/{selected_year}")

        if response.status_code == 200:
            response_data = response.json()
            # st.write(response_data)
            data = {
                "Month Number": list(response_data.keys()),
                "Month": [response_data[month]["month_name"] for month in response_data],
                "Total": [response_data[month]["total_amount"] for month in response_data],
                "Percentage": [response_data[month]["percentage"] for month in response_data]
            }

            df = pd.DataFrame(data)
            st.title("Expense breakdown by Month")
            st.bar_chart(data=df.set_index("Month")['Percentage'])
            df.set_index('Month Number',inplace=True)
            df.index.name = None
            st.table(df)
        else:
            st.error("no expenses available for the selected year")








