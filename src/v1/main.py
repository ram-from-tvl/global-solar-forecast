"""A Streamlit app to show global solar forecast."""
import json
import warnings

import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
import pycountry
import requests
import streamlit as st

data_dir = "src/v1/data"


@st.cache_data
def get_forecast(name:str, capacity:float, lat:float, lon:float) -> pd.Series:
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
        return forecast["predictions"]
    else:
        st.error(f"Error fetching forecast for {name}")


def main_page() -> None:
    """Main page, show a map of the world with the solar forecast."""
    st.header("Global Solar Forecast")

    # Lets load a map of the world
    world = gpd.read_file(f"{data_dir}/countries.geojson")

    # Get list of countries and their solar capcities now from the Ember API
    solar_capacity_per_country_df = pd.read_csv(f"{data_dir}/solar_capacities.csv", index_col=0)

    # remove nans in index
    solar_capacity_per_country_df["temp"] = solar_capacity_per_country_df.index
    solar_capacity_per_country_df.dropna(subset=["temp"], inplace=True)

    # add column with country code and name
    solar_capacity_per_country_df["country_code_and_name"] = \
        solar_capacity_per_country_df.index + " - " + solar_capacity_per_country_df["country_name"]

    # convert to dict
    solar_capacity_per_country = solar_capacity_per_country_df.to_dict()["capacity_gw"]
    global_solar_capacity = solar_capacity_per_country_df["capacity_gw"].sum()

    # drop down menu in side bar
    normalized = st.checkbox("Normalised each countries solar forecast (0-100%)", value=False)

    # run forecast for that countries
    forecast_per_country = {}
    my_bar = st.progress(0)
    countries = list(pycountry.countries)
    for i in range(len(countries)):
        my_bar.progress(int(i/len(countries)*100),
                        f"Loading Solar forecast for {countries[i].name} \
                        ({countries[i].alpha_3}) \
                        ({i+1}/{len(countries)})")
        country = countries[i]

        if country.alpha_3 not in solar_capacity_per_country:
            continue

        country_map = world[world["adm0_a3"] == country.alpha_3]
        if country_map.empty:
            continue

         # get centroid of country
         # # hide warning about GeoSeries.to_crs
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            centroid = country_map.geometry.to_crs(crs="EPSG:4326").centroid

        lat = centroid.y.values[0]
        lon = centroid.x.values[0]

        capacity = solar_capacity_per_country[country.alpha_3]
        forecast = get_forecast(country.name, capacity, lat, lon)

        if forecast:
            forecast = pd.DataFrame(forecast)
            forecast = forecast.rename(columns={"power_kw": "power_gw"})
            forecast_per_country[country.alpha_3] = forecast

            # display normalized forecast
            if normalized:
                forecast["power_gw"] = forecast["power_gw"] / capacity * 100

            forecast_per_country[country.alpha_3] = forecast

    my_bar.progress(100, "Loaded all forecasts.")
    my_bar.empty()


    # format forecast into pandas dataframe with columns, country code, timestamp, forecast_value
    all_forecasts = []
    for country_code, forecast in forecast_per_country.items():
        forecast["country_code"] = country_code
        all_forecasts.append(forecast)

    # concatenate all forecasts into a single dataframe
    all_forecasts = pd.concat(all_forecasts, ignore_index=False)
    all_forecasts.index.name = "timestamp"
    all_forecasts = all_forecasts.reset_index()

    # plot the total amount forecasted
    # group by country code and timestamp
    total_forecast = all_forecasts[["timestamp", "power_gw"]]
    total_forecast = total_forecast.groupby(["timestamp"]).sum().reset_index()

    # plot in ploty
    st.write(f"Global forecast, capacity of {global_solar_capacity} GW.")
    fig = go.Figure(data=go.Scatter(x=total_forecast["timestamp"],
                                    y=total_forecast["power_gw"],
                                    marker_color="#FF4901"))
    fig.update_layout(yaxis_title="Power [GW]", xaxis_title="Time")
    if not normalized:
        st.plotly_chart(fig)


    # now lets make a map plot, of the generation right now
    # get generation right now
    all_forecasts["timestamp"] = pd.to_datetime(all_forecasts["timestamp"])
    now = pd.Timestamp.utcnow().floor("h").replace(tzinfo=None)

    current_generation = all_forecasts[all_forecasts["timestamp"] == now]
    current_generation = current_generation[["country_code", "power_gw"]]

    # join 'world' and 'current_generation'
    world = world.merge(current_generation, how="left", left_on="adm0_a3", right_on="country_code")

    shapes_dict = json.loads(world.to_json())

    fig = go.Figure(data=go.Choroplethmap(
        geojson=shapes_dict,
        locations=world.index,
        z=world["power_gw"],
        colorscale="Viridis",
        colorbar_title="Power [GW]",
        marker_opacity=0.5,
    ))

    fig.update_layout(
                mapbox_style="carto-positron",
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                geo_scope="world",
            )
    st.plotly_chart(fig)

def country_page() -> None:
    """Country page, select a country and see the forecast for that country."""
    st.header("Country Page")
    st.write("This page will shows individual country forecasts")

    # Lets load a map of the world
    world = gpd.read_file(f"{data_dir}/countries.geojson")

    countries = list(pycountry.countries)

    # Get list of countries and their solar capcities now from the Ember API
    solar_capacity_per_country_df = pd.read_csv(f"{data_dir}/solar_capacities.csv", index_col=0)

    # remove nans in index
    solar_capacity_per_country_df["temp"] = solar_capacity_per_country_df.index
    solar_capacity_per_country_df.dropna(subset=["temp"], inplace=True)

    # add column with country code and name
    solar_capacity_per_country_df["country_code_and_name"] = \
        solar_capacity_per_country_df.index + " - " + solar_capacity_per_country_df["country_name"]

    # convert to dict
    solar_capacity_per_country = solar_capacity_per_country_df.to_dict()["capacity_gw"]
    country_code_and_names = list(solar_capacity_per_country_df["country_code_and_name"])

    selected_country = st.selectbox("Select a country:", country_code_and_names, index=0)
    selected_country_code = selected_country.split(" - ")[0]

    country = next(c for c in countries if c.alpha_3 == selected_country_code)

    country_map = world[world["adm0_a3"] == country.alpha_3]

        # get centroid of country
        # # hide warning about GeoSeries.to_crs
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        centroid = country_map.geometry.to_crs(crs="EPSG:4326").centroid

    lat = centroid.y.values[0]
    lon = centroid.x.values[0]

    capacity = solar_capacity_per_country[country.alpha_3]
    forecast = get_forecast(country.name, capacity, lat, lon)
    forecast = pd.DataFrame(forecast)
    forecast = forecast.rename(columns={"power_kw": "power_gw"})

     # plot in ploty
    st.write(f"{country.name} Solar Forecast, capacity of {capacity} GW.")
    fig = go.Figure(data=go.Scatter(x=forecast.index, y=forecast["power_gw"]))
    fig.update_layout(yaxis_title="Power [GW]", xaxis_title="Time")
    st.plotly_chart(fig)


def docs_page() -> None:
    """Documentation page."""
    st.header("Documentation")
    st.write("This page will show documentation (coming soon)")


if __name__ == "__main__":
    pg = st.navigation([
        st.Page(main_page, title="🌍 Global", default=True),
        st.Page(country_page, title="🏳️ Country"),
        st.Page(docs_page,title="📝 About"),
    ], position="top")
    pg.run()
