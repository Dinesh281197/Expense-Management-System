from datetime import datetime
import requests
import streamlit as st


st.title("Expense Management System")

API_URL =   "http://127.0.0.1:8000"

def add_update_tab():
    # --- 1. Select Date ---
    selected_date = st.date_input("Enter Date:", datetime(2024, 8, 2), label_visibility='collapsed')

    # --- 2. Initialize Session State ---
    if "num_rows" not in st.session_state:
        st.session_state.num_rows = 5
    if "previous_date" not in st.session_state:
        st.session_state.previous_date = None

    # --- 3. Fetch existing expenses from backend ---
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
        # st.write(existing_expenses)
    else:
        st.error("failed to retrieve responses")
        existing_expenses = []

    # --- 4. Reset number of rows if date has changed ---
    if st.session_state.previous_date != selected_date:
        st.session_state.num_rows = max(len(existing_expenses), 5)
        st.session_state.previous_date = selected_date

    # --- 5. Button to add more rows ---
    if st.button("+ Add Cell"):
        st.session_state.num_rows += 1

    # --- 6. Define category list ---
    categories=['Entertainment','Shopping','Food','Other','Rent','GYM', 'Investment']

    # --- 7. Begin form ---
    with st.form(key = "expense_form"):

        # Subheaders
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Amount")
        with col2:
            st.subheader("Category")
        with col3:
            st.subheader("Notes")

        # Store updated expense entries
        updated_expenses = []

        # --- 8. Render input fields ---
        for i in range(st.session_state.num_rows):
            # Prefill with existing or default values
            if i < len(existing_expenses):
                amount = existing_expenses[i]["amount"]
                category = existing_expenses[i]["category"]
                notes = existing_expenses[i]["notes"]
            else:
                amount = 0.0
                category = "Other"
                notes = ""

            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input =st.number_input(label = "Amount", min_value = 0.0, step =1.0,
                                              value = amount, key=f'amount_{i}', label_visibility= 'collapsed')
            with col2:
                category_input = st.selectbox(label = "Category", options = categories, index = categories.index(category) , key = f'category_{i}', label_visibility= 'collapsed')
            with col3:
                notes_input = st.text_input(label = "Notes", value = notes, key =f"notes_{i}", label_visibility= 'collapsed')

            updated_expenses.append({"amount": amount_input,
                                 "category": category_input,
                                 "notes": notes_input})

        submit_button = st.form_submit_button()

        # --- 9. Handle form submission ---
        if submit_button:

            filtered_values = [expense for expense in updated_expenses if expense['amount']>0 ]
            post_response = requests.post(f"{API_URL}/expenses/{selected_date}", json = filtered_values)
            if post_response.status_code == 200:
                st.success("Expenses updated Successfully!")
            else:
                st.error("Failed to update expenses.")

