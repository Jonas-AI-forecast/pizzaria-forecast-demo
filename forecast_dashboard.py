import streamlit as st
import pandas as pd
import altair as alt
import requests
from datetime import datetime
import locale

# === Hent data fra backend ===
URL = "https://pizzaria-backend-fghi.onrender.com/pizza-forecast-14d"

try:
    res = requests.get(URL)
    data = res.json()
except:
    st.error("⚠️ Kunne ikke hente data fra backend.")
    st.stop()

# === Opret DataFrame ===
df = pd.DataFrame(data)
df["dato"] = pd.to_datetime(df["dato"])

# === Manuelle danske oversættelser ===
danske_ugedage = {
    "Monday": "Mandag", "Tuesday": "Tirsdag", "Wednesday": "Onsdag",
    "Thursday": "Torsdag", "Friday": "Fredag", "Saturday": "Lørdag", "Sunday": "Søndag"
}
danske_måneder = {
    "January": "januar", "February": "februar", "March": "marts", "April": "april",
    "May": "maj", "June": "juni", "July": "juli", "August": "august",
    "September": "september", "October": "oktober", "November": "november", "December": "december"
}

df["dag_eng"] = df["dato"].dt.day_name()
df["måned_eng"] = df["dato"].dt.month_name()
df["dansk_dato"] = df["dag_eng"].map(danske_ugedage) + " d. " + df["dato"].dt.strftime("%d") + ". " + df["måned_eng"].map(danske_måneder)

# === Confidence interval kolonner ===
df["CI_bund"] = df["CI_lower"]
df["CI_top"] = df["CI_upper"]

# === Layout ===
st.set_page_config(layout="wide")
st.title("🍕 Glostrup Pizzaria 📊 Salgsforecast")

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("🗓️ Periode")
    st.write(f"{df['dato'].min().strftime('%A %d. %B')} → {df['dato'].max().strftime('%A %d. %B')}")

with col2:
    st.subheader("📊 Oversigt")
    st.metric("Gennemsnit", round(df["forudsagt_bestillinger"].mean(), 1))
    st.metric("Total", df["forudsagt_bestillinger"].sum())

    # Bonus
    st.metric("Højeste dag", df.loc[df["forudsagt_bestillinger"].idxmax()]["dansk_dato"])
    st.metric("Laveste dag", df.loc[df["forudsagt_bestillinger"].idxmin()]["dansk_dato"])

# === Visualisering ===
st.subheader("📈 Forudsigelser over 14 dage")
chart = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X("dansk_dato", title="Dato"),
    y=alt.Y("forudsagt_bestillinger", title="Antal bestillinger"),
    tooltip=["dansk_dato", "forudsagt_bestillinger", "CI_bund", "CI_top"]
).properties(height=400)

ci_band = alt.Chart(df).mark_area(opacity=0.2).encode(
    x="dansk_dato",
    y="CI_bund",
    y2="CI_top"
)

st.altair_chart(chart + ci_band, use_container_width=True)
