import pandas as pd
import numpy as np
import random

df = pd.read_csv("data/raw_stations.csv")
df.columns = df.columns.str.strip()

df = df[["name", "lattitude", "longitude"]]

df["lattitude"] = pd.to_numeric(
    df["lattitude"].astype(str).str.replace(",", ""),
    errors="coerce"
)

df["longitude"] = pd.to_numeric(
    df["longitude"].astype(str).str.replace(",", ""),
    errors="coerce"
)

df = df.dropna(subset=["lattitude", "longitude"])

df.columns = ["station_name", "latitude", "longitude"]

df["charging_power"] = np.random.choice([30, 50, 60], size=len(df))
df["total_slots"] = np.random.randint(5, 12, size=len(df))
occupied_list = []

for total in df["total_slots"]:
    occupied = random.randint(0, total)  # cannot exceed total
    occupied_list.append(occupied)

df["occupied_slots"] = occupied_list

df.to_csv("data/stations.csv", index=False)

print("✅ Clean dataset ready!")