"""The idea is to make a csv of all the solar capacites around the world.

The csv will countain
country_code, capacity_gw, country_name, source
"""

import pandas as pd

url = (
    "https://storage.googleapis.com/emb-prod-bkt-publicdata/public-downloads/"
    "yearly_full_release_long_format.csv"
)

# read csv into pandas dataframe
df = pd.read_csv(url)


# only select year 2024
df = df[df["Year"] == 2024]
# only select solar
df = df[df["Category"] == "Capacity"]
df = df[df["Variable"] == "Solar"]

df = df.rename(
    columns={"Value": "capacity_gw", "Area": "country_name", "ISO 3 code": "country_code"},
)
df = df[["country_code", "capacity_gw", "country_name"]]
df["source"] = "Ember"

df.set_index("country_code", inplace=True)

# manually add some countries not already present in the Ember dataset
# Additional countries with reliable sources from Wikipedia/Ember 2024 data
# All data sourced from https://en.wikipedia.org/wiki/Solar_power_by_country
manual_countries = {
    "UKR": {
        "country_name": "Ukraine",
        "capacity_gw": 1.2,
        "source": ("Wikipedia - https://en.wikipedia.org/wiki/Solar_power_by_country"),
    },
    "TJK": {
        "country_name": "Tajikistan",
        "capacity_gw": 0.0006,
        "source": "CABAR.asia 2024 (600 kW USAID project) - https://cabar.asia/en/tajikistan-solar-energy-in-support-of-hydropower-plants",
    },
    "TKM": {
        "country_name": "Turkmenistan",
        "capacity_gw": 0.005,
        "source": "UNDP 2012 Report - https://www.undp.org/sites/g/files/zskgke326/files/migration/eurasia/Turkmenistan.pdf",
    },
    "TLS": {
        "country_name": "Timor-Leste",
        "capacity_gw": 0.0011,
        "source": "Asian Development Bank sector assessment 2016–2020 - https://www.adb.org/sites/default/files/linked-documents/cps-tim-2016-2020-ssa-05.pdf",
    },
    "DZA": {
        "country_name": "Algeria",
        "capacity_gw": 0.46,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "SEN": {
        "country_name": "Senegal",
        "capacity_gw": 0.23,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "AGO": {
        "country_name": "Angola",
        "capacity_gw": 0.31,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "BEN": {
        "country_name": "Benin",
        "capacity_gw": 0.13,
        "source": "https://ember-energy.org/latest-insights/global-electricity-review-2025/",
    },
    "BFA": {
        "country_name": "Burkina Faso",
        "capacity_gw": 0.09,
        "source": "https://ember-energy.org/latest-insights/global-electricity-review-2025/",
    },
    "BDI": {
        "country_name": "Burundi",
        "capacity_gw": 0.017,
        "source": "https://ember-energy.org/latest-insights/global-electricity-review-2025/",
    },
    "CMR": {
        "country_name": "Cameroon",
        "capacity_gw": 0.09,
        "source": "https://ember-energy.org/latest-insights/the-first-evidence-of-a-take-off-in-solar-in-africa/",
    },
    "CPV": {
        "country_name": "Cape Verde",
        "capacity_gw": 0.026,
        "source": "IRENA 2023 via PV Magazine - https://www.pv-magazine.com/2024/11/14/cape-verde-runs-tender-for-10-mw-of-solar/",
    },
    "CAF": {
        "country_name": "Central African Republic",
        "capacity_gw": 0.01,
        "source": "https://ember-energy.org/latest-insights/the-first-evidence-of-a-take-off-in-solar-in-africa/",
    },
    "COM": {
        "country_name": "Comoros",
        "capacity_gw": 0.004034,
        "source": "IRENA 2023 via PVKnowhow - https://www.pvknowhow.com/solar-report/comoros/",
    },
    "DJI": {
        "country_name": "Djibouti",
        "capacity_gw": 0.02,
        "source": "https://ember-energy.org/latest-insights/global-electricity-review-2025/",
    },
    "ERI": {
        "country_name": "Eritrea",
        "capacity_gw": 0.01,
        "source": "https://ember-energy.org/latest-insights/the-first-evidence-of-a-take-off-in-solar-in-africa/",
    },
    "SWZ": {
        "country_name": "Eswatini",
        "capacity_gw": 0.03,
        "source": "https://www.globalsolarcouncil.org/news/global-solar-council-africas-solar-market-set-to-surge-42-in-2025-but-finance-bottlenecks-threaten-growth/",
    },
    "GAB": {
        "country_name": "Gabon",
        "capacity_gw": 0.01,
        "source": "https://ember-energy.org/latest-insights/the-first-evidence-of-a-take-off-in-solar-in-africa/",
    },
    "GMB": {
        "country_name": "Gambia",
        "capacity_gw": 0.03,
        "source": "https://www.pv-magazine.com/2023/02/10/gambia-inaugurates-23-mw-pv-plant/",
    },
    "GNQ": {
        "country_name": "Equatorial Guinea",
        "capacity_gw": 0.005,
        "source": "https://www.ren21.net/gsr-2025/downloads/pdf/go/GSR_2025_GO_2025_Full_Report.pdf",
    },
    "GIN": {
        "country_name": "Guinea",
        "capacity_gw": 0.01,
        "source": "https://ember-energy.org/latest-insights/global-electricity-review-2025/",
    },
    "GNB": {
        "country_name": "Guinea-Bissau",
        "capacity_gw": 0.005,
        "source": "https://www.ren21.net/gsr-2025/downloads/pdf/go/GSR_2025_GO_2025_Full_Report.pdf",
    },
    "CIV": {
        "country_name": "Ivory Coast",
        "capacity_gw": 0.05,
        "source": "https://ember-energy.org/latest-insights/global-electricity-review-2025/",
    },
    "LES": {
        "country_name": "Lesotho",
        "capacity_gw": 0.03,
        "source": "World Bank National Energy Compact 2025 - https://thedocs.worldbank.org/en/doc/038fd851752251bbd12392aa2a6d263c-0010012025/original/Lesotho-National-Energy-Compact-Mission-300.pdf",
    },
    "LSO": {
        "country_name": "Lesotho",
        "capacity_gw": 0.005,
        "source": "https://ember-energy.org/latest-insights/global-electricity-review-2025/",
    },
    "MRT": {
        "country_name": "Mauritania",
        "capacity_gw": 0.04,
        "source": "https://ember-energy.org/latest-insights/global-electricity-review-2025/",
    },
    "MWI": {
        "country_name": "Malawi",
        "capacity_gw": 0.03,
        "source": "https://www.ren21.net/gsr-2025/downloads/pdf/go/GSR_2025_GO_2025_Full_Report.pdf",
    },
    "STP": {
        "country_name": "Sao Tome and Principe",
        "capacity_gw": 0.0036,
        "source": "World Bank National Energy Compact 2025 - https://thedocs.worldbank.org/en/doc/680a427c0554b887598d86080fdcc775-0010012025/original/Sao-Tome-National-Energy-Compact-Mission-300.pdf",
    },
    "SLE": {
        "country_name": "Sierra Leone",
        "capacity_gw": 0.02,
        "source": "https://ember-energy.org/latest-insights/the-first-evidence-of-a-take-off-in-solar-in-africa/",
    },
    "SOM": {
        "country_name": "Somalia",
        "capacity_gw": 0.02,
        "source": "https://ember-energy.org/latest-insights/the-first-evidence-of-a-take-off-in-solar-in-africa/",
    },
    "SSD": {
        "country_name": "South Sudan",
        "capacity_gw": 0.0384,
        "source": "Combined: PVKnowhow 2025 (38.4 MW total) - https://www.pvknowhow.com/solar-report/south-sudan/",
    },
    "SYC": {
        "country_name": "Seychelles",
        "capacity_gw": 0.017,
        "source": "PVKnowhow 2024 Report - https://www.pvknowhow.com/solar-report/seychelles/",
    },
    "TCD": {
        "country_name": "Chad",
        "capacity_gw": 0.02,
        "source": "https://ember-energy.org/latest-insights/the-first-evidence-of-a-take-off-in-solar-in-africa/",
    },
    "ALB": {
        "country_name": "Albania",
        "capacity_gw": 0.21,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "COD": {
        "country_name": "Dem. Rep. Congo",
        "capacity_gw": 0.03,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "CUB": {
        "country_name": "Cuba",
        "capacity_gw": 0.28,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "GHA": {
        "country_name": "Ghana",
        "capacity_gw": 0.19,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "GTM": {
        "country_name": "Guatemala",
        "capacity_gw": 0.10,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "HND": {
        "country_name": "Honduras",
        "capacity_gw": 0.53,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "IDN": {
        "country_name": "Indonesia",
        "capacity_gw": 0.63,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "IRQ": {
        "country_name": "Iraq",
        "capacity_gw": 0.04,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "ISR": {
        "country_name": "Israel",
        "capacity_gw": 5.52,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "JOR": {
        "country_name": "Jordan",
        "capacity_gw": 2.59,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "LBN": {
        "country_name": "Lebanon",
        "capacity_gw": 1.00,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "MLI": {
        "country_name": "Mali",
        "capacity_gw": 0.10,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "MLT": {
        "country_name": "Malta",
        "capacity_gw": 0.244,
        "source": "Malta Regulator for Energy and Water 2024 - https://www.ceer.eu/wp-content/uploads/2024/07/C24_Malta-EN.pdf",
    },
    "MUS": {
        "country_name": "Mauritius",
        "capacity_gw": 0.147,
        "source": "Ministry of Energy Annual Report 2023-2024 - https://publicutilities.govmu.org/Documents/Annual%20Report2023-2024.pdf",
    },
    "NAM": {
        "country_name": "Namibia",
        "capacity_gw": 0.16,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "NPL": {
        "country_name": "Nepal",
        "capacity_gw": 0.25,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "PAN": {
        "country_name": "Panama",
        "capacity_gw": 0.65,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "SDN": {
        "country_name": "Sudan",
        "capacity_gw": 0.19,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "SGP": {
        "country_name": "Singapore",
        "capacity_gw": 1.348,
        "source": "Energy Market Authority Singapore 2024 - https://ema.gov.sg/resources/singapore-energy-statistics/chapter6",
    },
    "TGO": {
        "country_name": "Togo",
        "capacity_gw": 0.07,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "UZB": {
        "country_name": "Uzbekistan",
        "capacity_gw": 3.8,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "YEM": {
        "country_name": "Yemen",
        "capacity_gw": 0.29,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    "ZMB": {
        "country_name": "Zambia",
        "capacity_gw": 0.13,
        "source": (
            "Wikipedia (Ember 2024 data) - https://en.wikipedia.org/wiki/Solar_power_by_country"
        ),
    },
    # Our World in Data sources
    "ETH": {
        "country_name": "Ethiopia",
        "capacity_gw": 0.08,
        "source": (
            "Our World in Data - https://ourworldindata.org/grapher/installed-solar-pv-capacity"
        ),
    },
    "LBY": {
        "country_name": "Libya",
        "capacity_gw": 0.02,
        "source": (
            "Our World in Data - https://ourworldindata.org/grapher/installed-solar-pv-capacity"
        ),
    },
    "MDG": {
        "country_name": "Madagascar",
        "capacity_gw": 0.01,
        "source": (
            "Our World in Data - https://ourworldindata.org/grapher/installed-solar-pv-capacity"
        ),
    },
    "MOZ": {
        "country_name": "Mozambique",
        "capacity_gw": 0.01,
        "source": (
            "Our World in Data - https://ourworldindata.org/grapher/installed-solar-pv-capacity"
        ),
    },
    "RWA": {
        "country_name": "Rwanda",
        "capacity_gw": 0.12,
        "source": (
            "Our World in Data - https://ourworldindata.org/grapher/installed-solar-pv-capacity"
        ),
    },
    "TZA": {
        "country_name": "Tanzania",
        "capacity_gw": 0.02,
        "source": (
            "Our World in Data - https://ourworldindata.org/grapher/installed-solar-pv-capacity"
        ),
    },
    "UGA": {
        "country_name": "Uganda",
        "capacity_gw": 0.04,
        "source": (
            "Our World in Data - https://ourworldindata.org/grapher/installed-solar-pv-capacity"
        ),
    },
    "ZWE": {
        "country_name": "Zimbabwe",
        "capacity_gw": 0.09,
        "source": (
            "Our World in Data - https://ourworldindata.org/grapher/installed-solar-pv-capacity"
        ),
    },
    "AFG": {
        "country_name": "Afghanistan",
        "capacity_gw": 0.02,
        "source": (
            "Our World in Data - https://ourworldindata.org/grapher/installed-solar-pv-capacity"
        ),
    },
    "BHR": {
        "country_name": "Bahrain",
        "capacity_gw": 0.065,
        "source": "IEA Report 2024 via SAU Energy - https://www.saurenergy.me/emerging-middle-eastern-nations-to-advance-re-goals/",
    },
    "BTN": {
        "country_name": "Bhutan",
        "capacity_gw": 0.04,
        "source": (
            "Our World in Data - https://ourworldindata.org/grapher/installed-solar-pv-capacity"
        ),
    },
    "BWA": {
        "country_name": "Botswana",
        "capacity_gw": 0.006,
        "source": "www.pv-magazine.com/",
    },
    # --- Entries supplied by user on 2025-09-26 ---
    "ATA": {
        "country_name": "Antarctica",
        "capacity_gw": 0.0002,
        "source": "British Antarctic Survey renewable projects 2025 - https://www.bas.ac.uk/media-post/renewables-milestone-reached-in-antarctica/",
    },
    "BHS": {
        "country_name": "Bahamas",
        "capacity_gw": 0.002,
        "source": "IRENA Country Profile 2024 - https://www.irena.org/Data/Energy-Profiles",
    },
    "BLZ": {
        "country_name": "Belize",
        "capacity_gw": 0.002,
        "source": "IRENA Country Profile 2024 - https://www.irena.org/Data/Energy-Profiles",
    },
    "BRN": {
        "country_name": "Brunei",
        "capacity_gw": 0.005,
        "source": "IRENA Country Profile 2024 - https://www.irena.org/Data/Energy-Profiles",
    },
    "FLK": {
        "country_name": "Falkland Islands",
        "capacity_gw": 0.0034,
        "source": "Falkland Islands Energy Strategy & green-overseas.org - https://www.green-overseas.org/en/pays-et-territoires/falkland-islands",
    },
    "FJI": {
        "country_name": "Fiji",
        "capacity_gw": 0.011,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "ATF": {
        "country_name": "French Southern and Antarctic Lands",
        "capacity_gw": 0.0032,
        "source": "green-overseas.org & TAAF renewable energy installations - http://www.green-overseas.org/en/pays-et-territoires/french-southern-and-antarctic-lands",
    },
    "GRL": {
        "country_name": "Greenland",
        "capacity_gw": 0.001,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "GUY": {
        "country_name": "Guyana",
        "capacity_gw": 0.015,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "HTI": {
        "country_name": "Haiti",
        "capacity_gw": 0.004,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "ISL": {
        "country_name": "Iceland",
        "capacity_gw": 0.007,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "JAM": {
        "country_name": "Jamaica",
        "capacity_gw": 0.11,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "KOS": {
        "country_name": "Kosovo",
        "capacity_gw": 0.15,
        "source": "PVKnowhow 2024 & KfW Development Bank - https://www.pvknowhow.com/news/kosovo-solar-plant-keks-impressive-100-mw-project-begins/",
    },
    "LAO": {
        "country_name": "Laos",
        "capacity_gw": 0.059,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "LBR": {
        "country_name": "Liberia",
        "capacity_gw": 0.003,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "NCL": {
        "country_name": "New Caledonia",
        "capacity_gw": 0.185,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "NIC": {
        "country_name": "Nicaragua",
        "capacity_gw": 0.018,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "NER": {
        "country_name": "Niger",
        "capacity_gw": 0.08,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "PRK": {
        "country_name": "North Korea",
        "capacity_gw": 0.129,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "CYN": {
        "country_name": "Northern Cyprus",
        "capacity_gw": 0.0013,
        "source": "Research studies ETASR 2023 & ProLuxMax 2025 - https://etasr.com/index.php/ETASR/article/view/5744",
    },
    "PSX": {
        "country_name": "Palestine",
        "capacity_gw": 0.192,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "PNG": {
        "country_name": "Papua New Guinea",
        "capacity_gw": 0.004,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "PRY": {
        "country_name": "Paraguay",
        "capacity_gw": 0.001,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "COG": {
        "country_name": "Republic of the Congo",
        "capacity_gw": 0.001,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "SLB": {
        "country_name": "Solomon Islands",
        "capacity_gw": 0.004,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "SOL": {
        "country_name": "Somaliland",
        "capacity_gw": 0.0337,
        "source": "Combined projects - https://www.greenbuildingafrica.co.za/somaliland-issues-epc-tender-for-12mw-solar-bess-project-plus-13-5km-33kv-evacuation-line/",
    },
    "SDS": {
        "country_name": "South Sudan",
        "capacity_gw": 0.046,
        "source": "Combined sources - https://www.saurenergy.me/south-sudan-launches-first-solar-power-plant-with-bess/",
    },
    "SUR": {
        "country_name": "Suriname",
        "capacity_gw": 0.012,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "SYR": {
        "country_name": "Syria",
        "capacity_gw": 0.06,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "TTO": {
        "country_name": "Trinidad and Tobago",
        "capacity_gw": 0.004,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "VUT": {
        "country_name": "Vanuatu",
        "capacity_gw": 0.005,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "VEN": {
        "country_name": "Venezuela",
        "capacity_gw": 0.005,
        "source": "World Population Review 2025 - https://worldpopulationreview.com/country-rankings/solar-power-by-country",
    },
    "SAH": {
        "country_name": "Western Sahara",
        "capacity_gw": 0.1,
        "source": "WSRW Report 2024 - https://wsrw.org/en/news/renewable-energy",
    },
    "HKG": {
        "country_name": "Hong Kong",
        "capacity_gw": 0.19,
        "source": "TheGlobalEconomy (EIA) - https://www.theglobaleconomy.com/Hong-Kong/solar_electricity_capacity/",
    },
    "XKX": {
        "country_name": "Kosovo",
        "capacity_gw": 0.09,
        "source": "PVKnowhow 2025 Report - https://www.pvknowhow.com/news/kosovo-solar-energy-stunning-2025-advancements-proven/",
    },
}

manual_countries_df = pd.DataFrame.from_dict(manual_countries, orient="index")
manual_countries_df.index.name = "country_code"

df = pd.concat([df, manual_countries_df])

df.to_csv("solar_capacities.csv")
