# glostrup-pizzaria-api/train_model.py

import numpy as np
import pandas as pd
from xgboost import XGBRegressor
import joblib

print("🔥 Pizza training script is running!")

# === 1. Simuler pizzaria-data for Glostrup ===
days = 360
np.random.seed(77)  # Lås tilfældigheden for stabil data
data = pd.DataFrame({
    "dag_i_ugen": np.tile(np.arange(7), days // 7 + 1)[:days],
    "kampagne": np.random.choice([0, 1], size=days, p=[0.7, 0.3]),
    "vejr_temp": np.random.normal(loc=15, scale=7, size=days),
    "helligdag": np.random.choice([0, 1], size=days, p=[0.95, 0.05]),
    "regnvejr": np.random.choice([0, 1], size=days, p=[0.6, 0.4]),
    "weekend_aften": np.array([1 if i % 7 in [4, 5] else 0 for i in range(days)])
})

# === 2. Generér "antal bestillinger" som afhænger af features ===
data["antal_bestillinger"] = 100 \
    + data["kampagne"] * 40 \
    + data["regnvejr"] * 25 \
    + data["weekend_aften"] * 60 \
    - data["helligdag"] * 30 \
    + np.where(data["vejr_temp"] < 12, 15, 0) \
    + np.random.normal(0, 8, size=days)

# === 3. Træn modellen og gem den ===
X = data[["dag_i_ugen", "kampagne", "vejr_temp", "helligdag", "regnvejr", "weekend_aften"]]
y = data["antal_bestillinger"]

model = XGBRegressor(
    n_estimators=60,
    random_state=77,
    predictor='cpu_predictor',
    verbosity=0
)
model.fit(X, y)

joblib.dump(model, "pizza_model.joblib")
print("🍕 Pizza-model gemt som pizza_model.joblib")

# === Eksempel forudsigelse for test ===
print("🔍 Eksempel-predict:")
print(model.predict([[4, 1, 17.0, 0, 0, 1]]))  # Fredag m. kampagne, 17 grader, weekend aften
print("✅ Klar.")
