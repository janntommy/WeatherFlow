"""
Central configuration for the WeatherFlow project — the single source of truth
for the station list processed by the pipeline

Stations manually selected via find_stations.py (src/find_stations.py)
based on the official NOAA GHCN-Daily register (data/raw/stations.txt).
"""

TARGET_STATIONS = {
    "Warsaw": "PLM00012375",   # OKECIE
    "London": "UKM00003772",     # HEATHROW
    "New York": "USW00014786",  # FLOYD BENNETT FLD
    "Tokyo": "JA000047662",      # TOKYO
}

START_YEAR = 2021
END_YEAR = 2025