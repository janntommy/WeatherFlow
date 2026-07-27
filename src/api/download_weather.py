from pathlib import Path
import requests

URL = "https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_year"
DIR_PATH = Path("data/raw/by_year")

CHUNK_SIZE = 1024 * 1024    # 1MB

def download_single_year(year: int) -> Path:
    DIR_PATH.mkdir(parents=True, exist_ok=True)
    filepath = DIR_PATH / f"{year}.csv.gz"

    url = f"{URL}/{year}.csv.gz"
    response = requests.get(url, stream=True, timeout=100)
    response.raise_for_status()

    with open(filepath, "wb") as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            f.write(chunk)

    return filepath

def download_by_years(start_year: int, end_year: int) -> list[Path]:
    filepaths = []
    for year in range(start_year, end_year + 1):
        filepath = DIR_PATH / f"{year}.csv.gz"

        if filepath.exists():
            print(f"[{year}] Already downloaded")
        else:
            print(f"[{year}] Downloading from {URL}/{year}.csv.gz ...")
            filepath = download_single_year(year)
            print(f"[{year}] Downloaded - {filepath}")

        filepaths.append(filepath)
    return filepaths