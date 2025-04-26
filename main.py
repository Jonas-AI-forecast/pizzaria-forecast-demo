# Fil: main.py (backend)

from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import datetime
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

# === Sundhedstjek ===
@app.get("/", include_in_schema=False)
def health_check():
    return {"status": "ok"}


# === CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Indlæs model ===
model = joblib.load("pizza_model.joblib")

# === Sundhedstjek ===
@app.get("/")
def root():
    return {"message": "Backend kører!"}

# === Input-skema ===
class PizzaForecastInput(BaseModel):
    dag_i_ugen: int
    kampagne: int
    vejr_temp: float
    helligdag: int
    regnvejr: int
    weekend_aften: int

# === Output til 14-dages forecast ===
class PizzaForecastDay(BaseModel):
    dato: str
    forudsagt_bestillinger: int
    CI_lower: int
    CI_upper: int

# === Endpoint: Forecast for én dag ===
@app.post("/pizza-forecast")
def pizza_forecast(input: PizzaForecastInput):
    X = np.array([[
        input.dag_i_ugen,
        input.kampagne,
        input.vejr_temp,
        input.helligdag,
        input.regnvejr,
        input.weekend_aften
    ]])
    pred = model.predict(X)[0]
    return {
        "forudsagt_bestillinger": round(pred),
        "CI_lower": round(pred * 0.9),
        "CI_upper": round(pred * 1.1)
    }

# === Endpoint: 14-dages forecast ===
@app.get("/pizza-forecast-14d", response_model=list[PizzaForecastDay])
def pizza_forecast_14d():
    today = datetime.date.today()
    results = []
    vejr_temp = 17.0

    for i in range(14):
        dato = today + datetime.timedelta(days=i)
        dag_i_ugen = dato.weekday()

        rng = np.random.default_rng(seed=i)
        kampagne = int(rng.random() < 0.2)
        helligdag = 1 if dato.month == 12 and dato.day == 25 else 0
        regnvejr = int(rng.random() < 0.4)
        weekend_aften = int(dag_i_ugen in [4, 5])

        X = np.array([[dag_i_ugen, kampagne, vejr_temp, helligdag, regnvejr, weekend_aften]])
        pred = model.predict(X)[0]

        results.append({
            "dato": dato.isoformat(),
            "forudsagt_bestillinger": round(pred),
            "CI_lower": round(pred * 0.9),
            "CI_upper": round(pred * 1.1)
        })

    return results

# === Endpoint: Download forecast som Excel-fil ===
@app.get("/download-forecast")
def download_forecast():
    forecast = pizza_forecast_14d()
    df = pd.DataFrame(forecast)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Forecast')
    output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=forecast.xlsx"})
