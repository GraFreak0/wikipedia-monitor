import requests
import pandas as pd

def get_wikipedia_pageviews(article_title, start_date, end_date, project='en.wikipedia', granularity='daily'):
    """
    Fetch Wikipedia pageviews data from the Wikimedia REST API.

    :param article_title: Title of the article (use underscores instead of spaces)
    :param start_date: Start date in format YYYYMMDD
    :param end_date: End date in format YYYYMMDD
    :param project: Wikipedia project domain (default 'en.wikipedia')
    :param granularity: 'daily' or 'monthly'
    :return: pandas DataFrame with columns [domain_code, page_title, page_views, bytes, date]
    """

    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        f"{project}/all-access/all-agents/{article_title}/{granularity}/{start_date}/{end_date}"
    )

    headers = {
        "User-Agent": "WikipediaPageviewParser/1.0 (https://github.com/ghost; contact: ghost@example.com)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    data = response.json()
    items = data.get("items", [])

    records = []
    for item in items:
        records.append({
            "domain_code": project,
            "page_title": item["article"],
            "page_views": item["views"],
            "bytes": None, 
            "date": pd.to_datetime(item["timestamp"][:8], format='%Y%m%d')
        })

    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    df = get_wikipedia_pageviews(
        article_title="Apache_Airflow",
        start_date="20250101",
        end_date="20251001"
    )
    print(df.head())
