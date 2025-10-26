# Wikipedia Pageviews Analysis Workspace

This workspace is dedicated to collecting, processing, and analyzing Wikipedia pageviews data. It provides tools to fetch hourly dumps of all pageviews, retrieve pageviews for specific articles, get top-viewed pages over date ranges, and perform ETL transformations on the collected data. The goal is to enable data-driven insights into Wikipedia usage patterns, such as popular articles, traffic trends, and historical pageview statistics.

## Project Structure

- **`src/`**: Contains Python scripts for data fetching and processing.
  - `all-pages.py`: Fetches the latest available hourly Wikipedia pageviews dump (all pages), parses it into a pandas DataFrame, and saves it as a CSV file in the `dumps/` directory.
  - `page-views.py`: Retrieves pageviews data for a specific Wikipedia article using the Wikimedia REST API, returning a DataFrame with daily or monthly granularity.
  - `top-1000.py`: Fetches the top 1000 viewed Wikipedia pages for a specified date range, combines results into a single DataFrame, and exports to CSV in the `output/` directory.
- **`etl/`**: Contains Jupyter notebooks for data transformation and analysis.
  - `transform-all-per-hour.ipynb`: Loads multiple hourly dump CSV files from `dumps/`, concatenates them, and sorts the data by page views for analysis.
- **`dumps/`**: Directory for storing raw pageviews dump files (CSV format) fetched by `all-pages.py`.
- **`output/`**: Directory for processed output files, such as aggregated top pages data from `top-1000.py`.
- **`README.md`**: This file, providing an overview of the workspace.
- **`.gitignore`**: Specifies files and directories to ignore in version control (e.g., data files in `dumps/` and `output/`).

## Dependencies

- `pandas`: For data manipulation and DataFrame operations.
- `requests`: For making HTTP requests to Wikimedia APIs.
- `gzip`: For handling compressed dump files.
- `numpy`: Used in ETL transformations (imported in notebooks).
- `datetime` and `timedelta`: For date handling in scripts.

Install dependencies via pip:
```
pip install pandas requests numpy
```

## Usage

### Fetching Hourly Pageviews Dump
Run `src/all-pages.py` to download and parse the latest hourly pageviews dump:
```
python src/all-pages.py
```
- Attempts to fetch dumps up to 6 hours back from the current UTC time.
- Saves the parsed data as `wikipedia_pageviews_YYYYMMDD_HH.csv` in `dumps/`.
- Outputs a preview of the DataFrame and confirms the save.

### Fetching Pageviews for a Specific Article
Run `src/page-views.py` with parameters for an article:
```
python src/page-views.py
```
- Prompts for article title, start/end dates, etc., or uses defaults.
- Fetches data from the Wikimedia REST API and prints a preview.
- Example: Retrieves daily views for "Apache_Airflow" from 2025-01-01 to 2025-10-01.

### Fetching Top 1000 Pages for a Date Range
Run `src/top-1000.py`:
```
python src/top-1000.py
```
- Prompts for start and end dates (defaults to 2025-10-01 to 2025-10-05).
- Fetches top pages for each day in the range, combines into a DataFrame, sorts by date and views.
- Saves as `output/top_wikipedia_pages.csv`.
- Prints top 10 records and confirms save.

### ETL Transformation
Open `etl/transform-all-per-hour.ipynb` in Jupyter Notebook:
- Loads specified CSV files from `dumps/` (e.g., multiple hourly dumps).
- Concatenates them into a single DataFrame.
- Sorts by page views descending for analysis.
- Displays the sorted data for further processing or visualization.

## Data Format

All scripts output data in a consistent pandas DataFrame format with columns:
- `domain_code` or `project`: The Wikipedia project (e.g., 'en.wikipedia').
- `page_title`: Title of the page or article.
- `page_views`: Number of views.
- `bytes`: Size in bytes (available in dumps; None in API fetches).
- `date`: Timestamp or date of the data.

## Notes

- Respect Wikimedia's API usage policies: Include appropriate User-Agent headers and avoid excessive requests.
- Data is fetched in UTC; adjust for local timezones as needed.
- For large datasets, consider optimizing memory usage in pandas.
- This workspace is for educational and analytical purposes; ensure compliance with data usage terms.

## Contributing

Feel free to extend scripts for additional metrics, visualizations, or integrations (e.g., with databases or dashboards).
