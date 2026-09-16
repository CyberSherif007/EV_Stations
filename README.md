# EV_Stations
# ⚡ EV Range Prediction & Smart Charging Station Finder

A Python-based web application that combines **Machine Learning, EV data analysis, and geospatial services** to estimate an electric vehicle's driving range and help users find nearby charging stations.

The system predicts the expected full driving range of an EV using a **Support Vector Regression (SVR)** model and then estimates the remaining range based on the vehicle's current **State of Charge (SoC)**. It also identifies nearby charging stations and displays an interactive driving route to the nearest station.

---

## 🚀 Project Overview

Finding a suitable charging station while travelling in an electric vehicle can be challenging, especially when the remaining battery range is limited.

This project addresses the problem by combining:

- 🔋 EV range prediction
- 📊 Machine Learning
- 📍 Geospatial distance calculation
- ⚡ Charging station information
- 🗺️ Interactive maps and route visualization
- 🌐 Flask-based web application

The user provides their EV, current battery percentage, speed, travel distance, and location. The application estimates whether the destination is reachable and displays nearby charging stations.

---

## ✨ Key Features

### 🔋 EV Range Prediction
Uses a trained **Support Vector Regression (SVR)** model to predict EV range based on:

- Battery capacity
- Energy efficiency
- Vehicle speed

### 📉 Remaining Range Estimation

The predicted full range is adjusted according to the vehicle's current State of Charge:

```text
Remaining Range = Predicted Full Range × (SoC / 100)
