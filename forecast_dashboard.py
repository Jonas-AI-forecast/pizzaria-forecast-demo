import streamlit as st
import pandas as pd
import altair as alt
import requests
from datetime import datetime
import locale

# Forsøg at sætte dansk datoformat – fallback til engelsk hvis det fejler (fx på Render)
# Prøv dansk sprog - ellers brug engelsk fallback (Render tillader ikke "da_DK.UTF-8")
try:
    locale.setlocale(locale.LC_TIME, "da_DK.UTF-8")
except locale.Error:
    locale.setlocale(locale.LC_TIME, "en_US.UTF-8")


st.set_page_config(layout="wide")
st.title("🍕 Glostrup Pizzaria – Salgsforecast")

# --- Hent data fra backend ---
URL = "https://pizzaria-backend-fghi.onrender.com/pizza-forecast-14d"

try:
    res = requests.get(URL)
    data = res.json()
except:
    st.error("⚠️ Kunne ikke hente data fra backend.")
    st.stop()

df = pd.DataFrame(data)
df["dato"] = pd.to_datetime(df["dato"])
df["dag_navn"] = df["dato"].dt.strftime("%A %d. %B")
df["CI_bund"] = df["CI_lower"]
df["CI_top"] = df["CI_upper"]

# --- Layout ---
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("📅 Periode")
    st.write(f"{df['dato'].min().strftime('%A %d. %B')} → {df['dato'].max().strftime('%A %d. %B')}")

    st.subheader("📊 Oversigt")
    st.metric("Gennemsnit", f"{df['forudsagt_bestillinger'].mean():.1f}")
    st.metric("Total", int(df['forudsagt_bestillinger'].sum()))
    st.metric("Højeste dag", df.loc[df['forudsagt_bestillinger'].idxmax()]["dag_navn"])
    st.metric("Laveste dag", df.loc[df['forudsagt_bestillinger'].idxmin()]["dag_navn"])

    st.markdown("---")
    st.caption("Data opdateret automatisk ud fra vejr og dagstype")

with col2:
    st.subheader("📈 Forventet antal bestillinger de næste 14 dage")

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('dag_navn:N', sort=df['dag_navn'].tolist(), title='Dato'),
        y=alt.Y('forudsagt_bestillinger:Q', title='Bestillinger'),
        color=alt.Color('forudsagt_bestillinger:Q', scale=alt.Scale(scheme='yellowgreenblue'), legend=None),
        tooltip=['dag_navn', 'forudsagt_bestillinger', 'CI_lower', 'CI_upper']
    ).properties(width=700, height=400)

    st.altair_chart(chart, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("🔧 Bygget af Jonas – AI Forecast Demo © 2024")
