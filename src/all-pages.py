import requests
import pandas as pd
import gzip
import io
import os
from datetime import datetime, timedelta, timezone


def get_latest_available_wikipedia_dump(max_hours_back=6, dump_dir="dumps"):
    """
    Fetch and parse the latest available hourly Wikipedia pageviews dump (all pages).
    Tries up to `max_hours_back` hours backward from the last full UTC hour.
    Saves to `dump_dir` before parsing.
    """
    now_utc = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    headers = {"User-Agent": "WikipediaDumpFetcher/1.1 (contact: isaiah@example.com)"}

    os.makedirs(dump_dir, exist_ok=True)

    for i in range(max_hours_back):
        target_hour = now_utc - timedelta(hours=i + 1)
        year = target_hour.strftime("%Y")
        month = target_hour.strftime("%m")
        day = target_hour.strftime("%d")
        hour = target_hour.strftime("%H")

        dump_url = (
            f"https://dumps.wikimedia.org/other/pageviews/"
            f"{year}/{year}-{month}/pageviews-{year}{month}{day}-{hour}0000.gz"
        )
        print(f"Trying {dump_url} ...")

        response = requests.head(dump_url, headers=headers)
        if response.status_code == 200:
            print(f"Found available dump for {target_hour} UTC")
            return fetch_and_parse_dump(dump_url, target_hour, headers)

    raise Exception(f"No available dumps found in the last {max_hours_back} hours.")


def fetch_and_parse_dump(dump_url, timestamp, headers):
    """Download and parse the given dump file into a DataFrame."""
    print(f"Downloading {dump_url} ...")
    response = requests.get(dump_url, headers=headers, stream=True)
    response.raise_for_status()

    with gzip.open(io.BytesIO(response.content), "rt", encoding="utf-8") as f:
        df = pd.read_csv(
            f,
            sep=" ",
            names=["domain_code", "page_title", "page_views", "bytes"],
            dtype={
                "domain_code": str,
                "page_title": str,
                "page_views": int,
                "bytes": int,
            },
            on_bad_lines="skip",
        )

    df["date"] = timestamp
    print(f"✅ Parsed {len(df):,} rows from {timestamp} UTC")
    return df


if __name__ == "__main__":
    df = get_latest_available_wikipedia_dump(max_hours_back=6, dump_dir="dumps")
    print(df.head())

    filename = f"dumps/wikipedia_pageviews_{df['date'].iloc[0].strftime('%Y%m%d_%H')}.csv"
    df.to_csv(filename, index=False)
    print(f"\nSaved to {filename}")