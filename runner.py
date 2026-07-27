import argparse

from config.config import START_YEAR, END_YEAR
from src.api import download_weather, find_stations

CITIES_TO_SEARCH = ["LONDON", "HEATHROW", "NEW YORK", "CENTRAL PARK", "OKECIE", "TOKYO", "CNTRL PK"]


def run_find_stations():
    filepath = find_stations.DIR_PATH / "stations.txt"

    if not filepath.exists():
        print(f"Downloading stations list from... {find_stations.STATIONS_URL} ...")
        filepath = find_stations.download_stations_file()
        print(f"Saved: {filepath}")
    else:
        print(f"File already exists: {filepath}")

    df = find_stations.load_stations(filepath)
    print()
    print(f"Loaded {len(df):,} stations.")
    print()

    for city in CITIES_TO_SEARCH:
        results = find_stations.search_city(df, city)
        print(f"--- Results for '{city}' ({len(results)}) ---")
        if results.empty:
            print("  (NONE RESULTS FOUND)")
        else:
            print(results.to_string(index=False))
        print()


def download_weather_data():
    filepaths = download_weather.download_by_years(START_YEAR, END_YEAR)
    print()
    print(f"Download successful. {len(filepaths)} yearly files available in {download_weather.DIR_PATH}")

STEPS = {
    "find_stations": run_find_stations,
    "download_weather": download_weather_data(),
}


def run_all():
    for step_name, func in STEPS.items():
        print(f"\n=== Running step: {step_name} ===")
        func()


def main():
    parser = argparse.ArgumentParser(description="Runner for WeatherFlow programme")
    parser.add_argument(
        "--step",
        choices=list(STEPS.keys()) + ["all"],
        required=True,
        help="which step to run or 'all' to run all steps",
    )
    args = parser.parse_args()

    if args.step == "all":
        run_all()
    else:
        print(f"\n=== Running step: {args.step} ===")
        STEPS[args.step]()


if __name__ == "__main__":
    main()