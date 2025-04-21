# Fil: forecast_dashboard.py

import streamlit as st
import pandas as pd
import altair as alt
import requests
from datetime import datetime

# === Hent data fra online backend ===
URL = "https://pizzaria-backend-fghi.onrender.com/pizza-forecast-14d"  # <- Erstat med din rigtige URL

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

df["CI_bund"] = df["CI_lower"]
df["CI_top"] = df["CI_upper"]

# === Layout ===
st.set_page_config(layout="wide")
st.title("🍕 Glostrup Pizzaria 📊 Salgsforecast")

col1, col2 = st.columns([1.5, 1.5], gap="large")

with col1:
    st.subheader("🗓️ Periode")
    st.write(f"{df['dato'].min().strftime('%A %d. %B')} → {df['dato'].max().strftime('%A %d. %B')}")

    st.subheader("📋 Daglig tabel")
    styled_df = df[["dansk_dato", "forudsagt_bestillinger", "CI_bund", "CI_top"]].rename(columns={
        "dansk_dato": "Dato",
        "forudsagt_bestillinger": "Forventet salg",
        "CI_bund": "Nedre grænse",
        "CI_top": "Øvre grænse"
    }).set_index("Dato")

    st.markdown(
        styled_df.to_html(classes="styled-table", border=0),
        unsafe_allow_html=True
    )

    st.markdown("""
    <style>
    .styled-table {
        font-family: Arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        max-height: 300px;
        overflow-y: scroll;
        display: block;
    }
    .styled-table td, .styled-table th {
        border: 1px solid #ddd;
        padding: 8px;
        color: black !important;
    }
    .styled-table th {
        padding-top: 10px;
        padding-bottom: 10px;
        text-align: left;
        background-color: #f2f2f2;
        color: black !important;
        position: sticky;
        top: 0;
        background: #f2f2f2;
    }
    </style>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("📊 Oversigt")
    st.metric("Gennemsnit", round(df["forudsagt_bestillinger"].mean(), 1))
    st.metric("Total", df["forudsagt_bestillinger"].sum())
    st.metric("Højeste dag", df.loc[df["forudsagt_bestillinger"].idxmax()]["dansk_dato"])
    st.metric("Laveste dag", df.loc[df["forudsagt_bestillinger"].idxmin()]["dansk_dato"])

# === Dropdown for visningstype ===
st.subheader("📊 Vælg visningstype")
visning = st.selectbox("Vælg graf:", ["14-dages forecast", "Kun weekender", "Top 5 højeste forecasts"])

if visning == "14-dages forecast":
    df_vis = df.sort_values("dato")
elif visning == "Kun weekender":
    df_vis = df[df["dato"].dt.weekday >= 5]
elif visning == "Top 5 højeste forecasts":
    df_vis = df.sort_values("forudsagt_bestillinger", ascending=False).head(5).sort_values("dato")
else:
    df_vis = df.copy()

# === Visualisering ===
st.subheader("📈 Forudsigelser")
chart = alt.Chart(df_vis).mark_line(point=alt.OverlayMarkDef(filled=True, fill='blue', size=100)).encode(
    x=alt.X("dato:T", title="Dato"),
    y=alt.Y("forudsagt_bestillinger", title="Antal bestillinger"),
    tooltip=[
        alt.Tooltip("dansk_dato", title="Dato"),
        alt.Tooltip("forudsagt_bestillinger", title="Forventet salg"),
        alt.Tooltip("CI_bund", title="95% Nedre grænse"),
        alt.Tooltip("CI_top", title="95% Øvre grænse")
    ]
).properties(height=400)

ci_band = alt.Chart(df_vis).mark_area(opacity=0.2, color="lightblue").encode(
    x="dato:T",
    y="CI_bund",
    y2="CI_top"
)

st.altair_chart(chart + ci_band, use_container_width=True)

# === Forklaringsliste ===
st.subheader("📌 Forklaringer pr. dag")
for i, row in df_vis.iterrows():
    st.write(f"{row['dansk_dato']}: Automatisk analyse baseret på data")
