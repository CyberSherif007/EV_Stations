from flask import Flask, render_template, request
import pandas as pd
import folium
from geopy.distance import geodesic
import openrouteservice
import pickle   

app = Flask(__name__)

client = openrouteservice.Client(key="eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImY0Nzc3YjQwZGY5ODRkYzk5Zjk2NzFhYWNmYTkzM2Y4IiwiaCI6Im11cm11cjY0In0=")

# Load EV data
ev_data = pd.read_csv("data/ev_data.csv")
ev_data.columns = ev_data.columns.str.strip()
ev_data["car_name"] = ev_data["brand"] + " " + ev_data["model"]

# Load stations
stations = pd.read_csv("data/stations.csv")
stations.columns = stations.columns.str.strip()


model = pickle.load(open("model/model.pkl", "rb"))
scaler = pickle.load(open("model/scaler.pkl", "rb"))


def find_stations(user_location):
    station_list = []

    for _, row in stations.iterrows():
        try:
            lat = float(row["latitude"])
            lon = float(row["longitude"])

            distance = geodesic(user_location, (lat, lon)).km

            occupied = int(row["occupied_slots"])
            free = max(0, int(row["total_slots"]) - occupied)

            charging_time = round(1.5 / (row["charging_power"] / 50), 2)

            station_list.append({
                "name": row["station_name"],
                "lat": lat,
                "lon": lon,
                "distance": round(distance, 2),
                "free": free,
                "occupied": occupied,
                "time": charging_time
            })

        except:
            continue

    return sorted(station_list, key=lambda x: x["distance"])[:5]


@app.route("/")
def home():
    return render_template("index.html", cars=ev_data.to_dict(orient="records"))


@app.route("/predict", methods=["POST"])
def predict():
    car_name = request.form["car"]
    soc = float(request.form["soc"])
    speed = float(request.form["speed"])
    distance = float(request.form["distance"])

    lat = float(request.form["latitude"])
    lon = float(request.form["longitude"])
    user_location = (lat, lon)

    car = ev_data[ev_data["car_name"] == car_name].iloc[0]

    battery = car["battery_capacity_kWh"]
    efficiency = car["efficiency_wh_per_km"]

   
    input_data = [[battery, efficiency, speed]]
    input_scaled = scaler.transform(input_data)

    predicted_full_range = model.predict(input_scaled)[0]
    max_range = predicted_full_range * (soc / 100)

    reachable = max_range >= distance

    station_list = find_stations(user_location)
    best_station = station_list[0]

    # Map
    m = folium.Map(location=user_location, zoom_start=12)

    folium.Marker(user_location, tooltip="You").add_to(m)

    for s in station_list:
        folium.Marker([s["lat"], s["lon"]], tooltip=s["name"]).add_to(m)

    coords = [
        [user_location[1], user_location[0]],
        [best_station["lon"], best_station["lat"]]
    ]

    try:
        route = client.directions(
            coordinates=coords,
            profile="driving-car",
            format="geojson"
        )

        route_coords = route["features"][0]["geometry"]["coordinates"]
        route_latlon = [(c[1], c[0]) for c in route_coords]

        folium.PolyLine(route_latlon, color="blue", weight=5).add_to(m)

    except Exception as e:
        print("Route error:", e)

    map_html = m._repr_html_()

    return render_template(
        "result.html",
        range=round(max_range, 2),
        reachable=reachable,
        stations=station_list,
        map_html=map_html
    )


if __name__ == "__main__":
    app.run(debug=True)