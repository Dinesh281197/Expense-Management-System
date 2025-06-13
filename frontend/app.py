import streamlit as st
from view_add_update import view_add_update_tab
from analytics_by_category import analysis_by_category_tab
from analytics_by_month import analysis_by_month_tab

tab1, tab2, tab3 = st.tabs(["View/Add/Update","Analytics by Category", "Analytics by Month"])

with tab1:
    view_add_update_tab()

with tab2:
    analysis_by_category_tab()

with tab3:
    analysis_by_month_tab()



