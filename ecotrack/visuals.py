import pandas as pd
import streamlit as st

def show_breakdown(breakdown):
    st.markdown("### Emissions by category")
    chart = pd.DataFrame({"kg CO₂e": list(breakdown.values())}, index=list(breakdown.keys()))
    st.bar_chart(chart)
    st.dataframe(chart, use_container_width=True)
