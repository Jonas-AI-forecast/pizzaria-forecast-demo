import streamlit as st
import pandas as pd
import requests
import altair as alt
import datetime

st.set_page_config(page_title="🍕 Pizza Forecast Dashboard", layout="wide")
st.title("🍕 Glostrup Pizzaria – Interaktivt 14-dages Forecast")

# === Hent og vis live vejr ===
vejr_url = "https://api.openweathermap.org/data/2.5/weather?lat=55.6667&lon=12.4000&units=metric&appid=4c8b4631a40e4e0d4a2be5ee2023e241"
vejr_data = requests.get(vejr_url).json()

try:
    temp = vejr_data['main']['temp']
    beskrivelse = vejr_data['weather'][0]['description']
except KeyError:
    temp = 14.0
    beskrivelse = "Ukendt"

st.markdown(f"### 🌦️ Aktuelt vejr i Glostrup: **{temp:.1f}°C** – *{beskrivelse.title()}*")

# === Hent 14-dages forecast fra API ===
with st.spinner("Henter forecast fra AI..."):
    res = requests.get("http://127.0.0.1:8000/pizza-forecast-14d")
    data = res.json()
    df = pd.DataFrame(data)

# === Tilføj rigtige datoer for kampagnedropdown ===
df['dato_dag'] = pd.to_datetime(df['dato']).dt.strftime('%d. %b')

# === Brugerinput ===
st.sidebar.header("🔧 Justér scenarier")
vejr_temp = st.sidebar.slider("Gennemsnitlig temperatur (°C)", min_value=5, max_value=30, value=15)
regnvejr = st.sidebar.checkbox("Regnvejr?", value=False)

kampagnedage = st.sidebar.multiselect(
    "📅 Vælg kampagnedage:",
    options=df['dato_dag'].tolist(),
    default=[]
)

# === Brug justeringer ===
for i in range(len(df)):
    if df.loc[i, 'dato_dag'] in kampagnedage:
        df.at[i, 'forudsagt_bestillinger'] += 25
if regnvejr:
    df['forudsagt_bestillinger'] += 15

df['CI_lower'] = (df['forudsagt_bestillinger'] * 0.9).astype(int)
df['CI_upper'] = (df['forudsagt_bestillinger'] * 1.1).astype(int)

# === Vis tabel ===
st.subheader("📋 Forecast tabel")
st.dataframe(df)

# === Vis graf ===
st.subheader("📊 Søjlediagram med usikkerhed")
bar_chart = alt.Chart(df).mark_bar(size=30).encode(
    x=alt.X('dato:N', title='Dato'),
    y=alt.Y('forudsagt_bestillinger:Q', title='Bestillinger'),
    color=alt.condition(
        alt.datum.forudsagt_bestillinger > 230,
        alt.value('#ff6961'),
        alt.value('#4caf50')
    ),
    tooltip=['dato', 'forudsagt_bestillinger', 'CI_lower', 'CI_upper']
).properties(width=900, height=400)

ci_band = alt.Chart(df).mark_errorbar(extent='ci').encode(
    x='dato:N',
    y='CI_lower:Q',
    y2='CI_upper:Q'
)

st.altair_chart(bar_chart + ci_band, use_container_width=True)

# === Download-knap ===
st.subheader("📥 Download forecast som Excel")
excel_df = df.copy()
excel_file = excel_df.to_excel(index=False)

st.download_button(
    label="Download Excel-fil",
    data=excel_file,
    file_name="pizza_forecast.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.info("💡 Flere funktioner kommer: integreret vagtplan, lokal vejr-API, PDF-download og meget mere!")
