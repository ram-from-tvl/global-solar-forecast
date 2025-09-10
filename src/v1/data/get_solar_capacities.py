"""The idea is to make a csv of all the solar capacites around the world.

The csv will countain
country_code, capacity_gw, country_name, source
"""

import pandas as pd

url = "https://storage.googleapis.com/emb-prod-bkt-publicdata/public-downloads/yearly_full_release_long_format.csv"

# read csv into pandas dataframe
df = pd.read_csv(url)


# only select year 2024
df = df[df["Year"] == 2024]
# only select solar
df = df[df["Category"] == "Capacity"]
df = df[df["Variable"] == "Solar"]

df = df.rename(columns={"Value": "capacity_gw",
                        "Area": "country_name",
                        "ISO 3 code": "country_code"})
df = df[["country_code", "capacity_gw", "country_name"]]
df["source"] = "Ember"

df.set_index("country_code", inplace=True)

# manually add some countries
# Lots more to add ...
manual_countries = {
    "UKR": {"country_name": "Ukraine", "capacity_gw": 1.2, "source": "Wikipedia"},
    "TKM": {"country_name": "Turkmenistan", "capacity_gw": 0.0,
            "source": "www.theglobaleconomy.com"},
    "DZA": {"country_name": "Algeria", "capacity_gw": 0.46, "source": "Wikipedia"},
    "SEN": {"country_name": "Senegal", "capacity_gw": 0.26, "source": "Wikipedia"},
}

manual_countries_df = pd.DataFrame.from_dict(manual_countries, orient="index")
manual_countries_df.index.name = "country_code"

df = pd.concat([df, manual_countries_df])

df.to_csv("src/v1/data/solar_capacities.csv")
