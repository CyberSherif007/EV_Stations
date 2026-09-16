import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import pickle

df = pd.read_csv("data/ev_data.csv")

X = df[["battery_capacity_kWh", "efficiency_wh_per_km", "top_speed_kmh"]]
y = df["range_km"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = SVR(kernel="rbf")
model.fit(X_scaled, y)

pickle.dump(model, open("model/model.pkl", "wb"))
pickle.dump(scaler, open("model/scaler.pkl", "wb"))

print("✅ Model trained!")