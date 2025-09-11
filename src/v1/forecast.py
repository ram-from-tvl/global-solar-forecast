"""Functions to get solar forecast data."""
from typing import Any

import pandas as pd
import requests
import streamlit as st

data_dir = "src/v1/data"


@st.cache_data
def get_forecast(
    name: str, capacity: float, lat: float, lon: float,
) -> list[dict[str, Any]] | None:
    """Get solar forecast for a given location and capacity."""
    if capacity == 0:
        return None

    site = {
        "latitude": lat,
        "longitude": lon,
        "capacity_kwp": capacity,
        "tilt": abs(lat) / 2,
        "orientation": 180 if lat > 0 else 0,
    }
    now = pd.Timestamp.utcnow().floor("h").replace(tzinfo=None).isoformat()
    data = {"site": site, "timestamp": now}
    url = "https://open.quartz.solar/forecast/"

    r = requests.post(url, json=data, timeout=20)

    if r.status_code == 200:
        forecast = r.json()
        predictions: list[dict[str, Any]] = forecast["predictions"]
        return predictions
    else:
        st.error(f"Error fetching forecast for {name}")
        return None
