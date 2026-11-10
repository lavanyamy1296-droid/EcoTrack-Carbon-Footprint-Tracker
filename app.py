import streamlit as st
import pandas as pd
from datetime import date
from ecotrack.calculator import calculate_footprint, get_recommendations
from ecotrack.visuals import show_breakdown

st.set_page_config(page_title="EcoTrack | Carbon Footprint Tracker", page_icon="🌱", layout="wide")
st.markdown("""
<style>
.block-container{max-width:1180px;padding-top:1.8rem}
.hero{padding:1.7rem 2rem;border-radius:20px;color:white;background:linear-gradient(120deg,#123c35,#21866b);margin-bottom:1.25rem}
.hero h1{color:white;margin:0}.hero p{color:#e1fff4;margin:.5rem 0 0}
</style>
<div class="hero"><h1>🌱 EcoTrack</h1><p>Understand your estimated carbon footprint. Discover practical ways to reduce it.</p></div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🌍 EcoTrack")
    page = st.radio("Navigate", ["My Footprint", "History", "About & Method"])
    st.caption("Personal carbon estimate • Educational project")

if "records" not in st.session_state:
    st.session_state.records = []

if page == "My Footprint":
    st.subheader("Your activity for one month")
    st.write("Enter approximate monthly usage. Use zero for anything that does not apply.")
    with st.form("footprint_form"):
        left, right = st.columns(2)
        with left:
            st.markdown("### ⚡ Home energy")
            electricity = st.number_input("Electricity (kWh/month)", 0.0, 100000.0, 120.0, 5.0)
            lpg = st.number_input("LPG (kg/month)", 0.0, 10000.0, 14.2, 0.5)
            st.markdown("### 🚗 Transport")
            car = st.number_input("Car travel (km/month)", 0.0, 100000.0, 250.0, 10.0)
            bike = st.number_input("Two-wheeler travel (km/month)", 0.0, 100000.0, 300.0, 10.0)
            bus = st.number_input("Bus travel (passenger-km/month)", 0.0, 100000.0, 100.0, 10.0)
            train = st.number_input("Train travel (passenger-km/month)", 0.0, 100000.0, 50.0, 10.0)
        with right:
            st.markdown("### 🍽️ Food")
            diet = st.selectbox("Usual diet", ["Mostly plant-based", "Mixed diet", "Meat-heavy"])
            st.markdown("### 🗑️ Waste")
            waste = st.number_input("Household waste (kg/month)", 0.0, 10000.0, 20.0, 1.0)
            recycling = st.selectbox("Do you regularly recycle?", ["Yes", "Sometimes", "No"])
            report_date = st.date_input("Month represented", value=date.today())
        submitted = st.form_submit_button("Calculate my footprint 🌿", type="primary", use_container_width=True)

    if submitted:
        activity = {"electricity_kwh": electricity, "lpg_kg": lpg, "car_km": car,
                    "two_wheeler_km": bike, "bus_passenger_km": bus,
                    "train_passenger_km": train, "diet": diet, "waste_kg": waste,
                    "recycling": recycling}
        result = calculate_footprint(activity)
        record = {"date": report_date.isoformat(), **activity, **result}
        st.session_state.latest = record
        st.session_state.records.insert(0, record.copy())

    if "latest" in st.session_state:
        result = st.session_state.latest
        st.divider()
        st.subheader("Your estimated monthly footprint")
        a, b, c = st.columns(3)
        a.metric("Total emissions", f'{result["total_kg"]:.1f} kg CO₂e')
        b.metric("Annualized estimate", f'{result["total_kg"]*12/1000:.2f} tonnes CO₂e')
        c.metric("Largest category", result["largest_category"])
        chart_col, tips_col = st.columns([1, 1])
        with chart_col:
            show_breakdown(result["breakdown"])
        with tips_col:
            st.markdown("### 🌱 Personalized reduction ideas")
            for tip in get_recommendations(result):
                st.markdown(f"- {tip}")
        st.caption("Indicative estimate only—not a verified carbon audit. Actual emissions vary by location, energy source, vehicle and consumption patterns.")

elif page == "History":
    st.subheader("Your saved calculations")
    if st.session_state.records:
        frame = pd.DataFrame([{"Month": r["date"], "Total (kg CO₂e)": round(r["total_kg"], 2),
                               "Largest category": r["largest_category"]} for r in st.session_state.records])
        st.dataframe(frame, use_container_width=True, hide_index=True)
        st.download_button("Download history as CSV", frame.to_csv(index=False).encode("utf-8"),
                           "ecotrack_history.csv", "text/csv")
        if st.button("Clear session history"):
            st.session_state.records = []
            st.session_state.pop("latest", None)
            st.rerun()
    else:
        st.info("No calculations saved in this browser session yet. Calculate your first estimate under My Footprint.")

else:
    st.subheader("About EcoTrack")
    st.write("EcoTrack converts everyday activity inputs into indicative CO₂-equivalent estimates and suggests practical reduction actions.")
    st.code("Estimated emissions (kg CO₂e) = activity amount × emission factor")
    st.markdown("### Simplified illustrative factors")
    st.dataframe(pd.DataFrame([
        ["Electricity", "kWh", 0.70], ["LPG", "kg", 3.00], ["Car", "km", 0.18],
        ["Two-wheeler", "km", 0.07], ["Bus", "passenger-km", 0.08],
        ["Train", "passenger-km", 0.04], ["Waste", "kg", 0.50]
    ], columns=["Activity", "Input unit", "Illustrative kg CO₂e factor"]), use_container_width=True, hide_index=True)
    st.markdown("""
    **Limitations:** These are simplified teaching defaults, not official location-specific factors.
    Food is represented by a broad diet proxy. Recycling changes advice but does not subtract an assumed
    avoided-emissions credit. For formal research, replace defaults with documented factors for the
    relevant geography, year and system boundary. Shared household energy should be apportioned fairly.
    """)
