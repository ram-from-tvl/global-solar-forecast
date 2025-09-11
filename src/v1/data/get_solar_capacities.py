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
# Additional countries with reliable sources from Wikipedia/Ember 2024 data
# All data sourced from https://en.wikipedia.org/wiki/Solar_power_by_country (Ember Climate 2024 data)
manual_countries = {
    "UKR": {"country_name": "Ukraine", "capacity_gw": 1.2, "source": "Wikipedia"},
    "TKM": {"country_name": "Turkmenistan", "capacity_gw": 0.0,
            "source": "www.theglobaleconomy.com"},
    "DZA": {"country_name": "Algeria", "capacity_gw": 0.46, "source": "Wikipedia/Ember 2024 data"},
    "SEN": {"country_name": "Senegal", "capacity_gw": 0.23, "source": "Wikipedia/Ember 2024 data"},
    "AGO": {"country_name": "Angola", "capacity_gw": 0.31, "source": "Wikipedia/Ember 2024 data"},
    "ALB": {"country_name": "Albania", "capacity_gw": 0.21, "source": "Wikipedia/Ember 2024 data"},
    "ARM": {"country_name": "Armenia", "capacity_gw": 0.49, "source": "Wikipedia/Ember 2024 data"},
    "AZE": {"country_name": "Azerbaijan", "capacity_gw": 0.29, "source": "Wikipedia/Ember 2024 data"},
    "BGD": {"country_name": "Bangladesh", "capacity_gw": 0.85, "source": "Wikipedia/Ember 2024 data"},
    "BIH": {"country_name": "Bosnia and Herzegovina", "capacity_gw": 0.21, "source": "Wikipedia/Ember 2024 data"},
    "BLR": {"country_name": "Belarus", "capacity_gw": 0.26, "source": "Wikipedia/Ember 2024 data"},
    "COD": {"country_name": "Dem. Rep. Congo", "capacity_gw": 0.03, "source": "Wikipedia/Ember 2024 data"},
    "CUB": {"country_name": "Cuba", "capacity_gw": 0.28, "source": "Wikipedia/Ember 2024 data"},
    "GHA": {"country_name": "Ghana", "capacity_gw": 0.19, "source": "Wikipedia/Ember 2024 data"},
    "GTM": {"country_name": "Guatemala", "capacity_gw": 0.10, "source": "Wikipedia/Ember 2024 data"},
    "HND": {"country_name": "Honduras", "capacity_gw": 0.53, "source": "Wikipedia/Ember 2024 data"},
    "IDN": {"country_name": "Indonesia", "capacity_gw": 0.63, "source": "Wikipedia/Ember 2024 data"},
    "IRQ": {"country_name": "Iraq", "capacity_gw": 0.04, "source": "Wikipedia/Ember 2024 data"},
    "ISR": {"country_name": "Israel", "capacity_gw": 5.52, "source": "Wikipedia/Ember 2024 data"},
    "JOR": {"country_name": "Jordan", "capacity_gw": 2.59, "source": "Wikipedia/Ember 2024 data"},
    "KAZ": {"country_name": "Kazakhstan", "capacity_gw": 1.20, "source": "Wikipedia/Ember 2024 data"},
    "KEN": {"country_name": "Kenya", "capacity_gw": 0.37, "source": "Wikipedia/Ember 2024 data"},
    "KWT": {"country_name": "Kuwait", "capacity_gw": 0.10, "source": "Wikipedia/Ember 2024 data"},
    "LBN": {"country_name": "Lebanon", "capacity_gw": 1.00, "source": "Wikipedia/Ember 2024 data"},
    "MAR": {"country_name": "Morocco", "capacity_gw": 0.93, "source": "Wikipedia/Ember 2024 data"},
    "MDA": {"country_name": "Moldova", "capacity_gw": 0.34, "source": "Wikipedia/Ember 2024 data"},
    "MLI": {"country_name": "Mali", "capacity_gw": 0.10, "source": "Wikipedia/Ember 2024 data"},
    "MNG": {"country_name": "Mongolia", "capacity_gw": 0.14, "source": "Wikipedia/Ember 2024 data"},
    "MUS": {"country_name": "Mauritius", "capacity_gw": 0.13, "source": "Wikipedia/Ember 2024 data"},
    "MMR": {"country_name": "Myanmar", "capacity_gw": 0.22, "source": "Wikipedia/Ember 2024 data"},
    "NAM": {"country_name": "Namibia", "capacity_gw": 0.16, "source": "Wikipedia/Ember 2024 data"},
    "NGA": {"country_name": "Nigeria", "capacity_gw": 0.14, "source": "Wikipedia/Ember 2024 data"},
    "NPL": {"country_name": "Nepal", "capacity_gw": 0.25, "source": "Wikipedia/Ember 2024 data"},
    "NZL": {"country_name": "New Zealand", "capacity_gw": 0.57, "source": "Wikipedia/Ember 2024 data"},
    "OMN": {"country_name": "Oman", "capacity_gw": 0.67, "source": "Wikipedia/Ember 2024 data"},
    "PAN": {"country_name": "Panama", "capacity_gw": 0.65, "source": "Wikipedia/Ember 2024 data"},
    "PER": {"country_name": "Peru", "capacity_gw": 0.53, "source": "Wikipedia/Ember 2024 data"},
    "SDN": {"country_name": "Sudan", "capacity_gw": 0.19, "source": "Wikipedia/Ember 2024 data"},
    "TGO": {"country_name": "Togo", "capacity_gw": 0.07, "source": "Wikipedia/Ember 2024 data"},
    "TUN": {"country_name": "Tunisia", "capacity_gw": 0.77, "source": "Wikipedia/Ember 2024 data"},
    "URY": {"country_name": "Uruguay", "capacity_gw": 0.33, "source": "Wikipedia/Ember 2024 data"},
    "UZB": {"country_name": "Uzbekistan", "capacity_gw": 3.8, "source": "Wikipedia/Ember 2025 data"},
    "YEM": {"country_name": "Yemen", "capacity_gw": 0.29, "source": "Wikipedia/Ember 2024 data"},
    "ZMB": {"country_name": "Zambia", "capacity_gw": 0.13, "source": "Wikipedia/Ember 2024 data"},
}

manual_countries_df = pd.DataFrame.from_dict(manual_countries, orient="index")
manual_countries_df.index.name = "country_code"

df = pd.concat([df, manual_countries_df])

df.to_csv("src/v1/data/solar_capacities.csv")
