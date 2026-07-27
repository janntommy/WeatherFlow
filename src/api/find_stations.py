import requests
import numpy as np
import pandas as pd
from pathlib import Path

STATIONS_URL = "https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt"
DIR_PATH = Path("data/raw")

COLS = [(0, 11),  # ID
        (12, 20),  # LATITUDE
        (21, 30),  # LONGITUDE
        (31, 37),  # ELEVATION
        (38, 40),  # STATE
        (41, 71),  # NAME
        (72, 75),  # GSN FLAG
        (76, 79),  # HCN/CRN FLAG
        (80, 85)]  # WMO ID

COLUMN_NAMES = [
    "station_id",
    "latitude",
    "longitude",
    "elevation",
    "state",
    "name",
    "gsn_flag",
    "hcn_crn_flag",
    "wmo_id"
]


def download_stations_file() -> Path:
    DIR_PATH.mkdir(parents=True, exist_ok=True)
    filepath = DIR_PATH / "stations.txt"

    response = requests.get(STATIONS_URL, timeout=60)
    response.raise_for_status()

    filepath.write_bytes(response.content)
    return filepath


def load_stations(path: Path) -> pd.DataFrame:
    df = pd.read_fwf(path, colspecs=COLS, names=COLUMN_NAMES)


    for col in ["station_id", "state", "name", "gsn_flag", "hcn_crn_flag", "wmo_id"]:
        df[col] = df[col].astype(str).str.strip()
    return df


def search_city(df: pd.DataFrame, city_name: str) -> pd.DataFrame:
    mask = df["name"].str.contains(city_name, case=False, na=False)
    return df[mask][["station_id", "name", "state", "latitude", "longitude", "elevation"]]