import requests
import pandas as pd
from datetime import datetime, timedelta

def get_top_wikipedia_pages_for_range(project="en.wikipedia", access="all-access",
                                      start_date="2025-10-01", end_date="2025-10-05"):
    """
    Fetch top 1000 viewed Wikipedia pages for a date range using Wikimedia REST API.
    Combines results into a single DataFrame.

    :param project: Wikipedia project domain (e.g., 'en.wikipedia')
    :param access: 'all-access', 'desktop', 'mobile-app', or 'mobile-web'
    :param start_date: Start date in format YYYY-MM-DD
    :param end_date: End date in format YYYY-MM-DD
    :return: pandas DataFrame with columns [project, page_title, page_views, bytes, date]
    """
    headers = {
        "User-Agent": "WikipediaAnalytics/2.0 (contact: ghost@ghost.com)"
    }

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    all_records = []

    current = start
    while current <= end:
        year = current.strftime("%Y")
        month = current.strftime("%m")
        day = current.strftime("%d")

        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/{project}/{access}/{year}/{month}/{day}"
        print(f"Fetching data for {year}-{month}-{day}...")

        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            print(f"No data found for {year}-{month}-{day}. Skipping.")
            current += timedelta(days=1)
            continue
        elif response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")

        data = response.json()
        articles = data['items'][0]['articles']

        for article in articles:
            all_records.append({
                "project": project,
                "page_title": article['article'],
                "page_views": article['views'],
                "bytes": None,  # not provided by REST API
                "date": f"{year}-{month}-{day}"
            })

        current += timedelta(days=1)

    df = pd.DataFrame(all_records)
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(['date', 'page_views'], ascending=[True, False])

    return df

if __name__ == "__main__":
    stDate = input("Enter start date (YYYY-MM-DD): ") or "2025-10-01"
    enDate = input("Enter end date (YYYY-MM-DD): ") or "2025-10-05"

    df = get_top_wikipedia_pages_for_range(
        project="en.wikipedia",
        access="all-access",
        start_date=stDate,
        end_date=enDate
    )

    print("\nTop 10 records:")
    print(df.head(10))

    df.to_csv("output/top_wikipedia_pages.csv", index=False)
    print("\nSaved to top_wikipedia_pages.csv ✅")
