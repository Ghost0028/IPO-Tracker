import logging
import sys
import time
from io import StringIO
from datetime import datetime, date

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging once at the top
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

urls = [
    "https://www.investorgain.com/report/live-ipo-gmp/331/",
    "https://ipowatch.in/ipo-subscription-status-today/"
]


def modify_ipo_date(date_str):
    """Convert '30-Dec' style strings to datetime objects, handle NaN/missing values."""
    current_year = date.today().year
    current_month = date.today().month
    current_date = date.today().day

    if pd.isna(date_str) or date_str is None:
        return datetime(current_year - 1, current_month, current_date)

    date_str = str(date_str).strip()
    if not date_str or date_str.lower() in ['nan', 'none', 'null']:
        return datetime(current_year - 1, current_month, current_date)

    if '-' not in date_str:
        return datetime(current_year - 1, current_month, current_date)

    close_date, month_str = date_str.split('-')[:2]
    month_str = month_str.split(' ')[0]

    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }

    month = month_map.get(month_str)
    if not month:
        logging.warning(f"Unknown month string: {month_str}")
        return datetime(current_year - 1, current_month, current_date)

    if current_month != 12:
        return datetime(current_year, month, int(close_date))
    elif current_month == 12 and month == 1:
        return datetime(current_year + 1, month, int(close_date))
    else:
        return datetime(current_year, month, int(close_date))


def scrape_url(url, idx):
    """Scrape a single URL and return the first table as a DataFrame."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    logging.info(f"Launching Chrome driver {idx} for {url}")
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        logging.exception("Failed to start Chrome driver")
        sys.exit(1)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        logging.info("Table detected!")
        time.sleep(3)  # allow JS to load
        dfs = pd.read_html(StringIO(driver.page_source))
        return dfs[0]
    except Exception as e:
        logging.exception(f"Failed to scrape {url}")
        return None
    finally:
        driver.quit()


def merge_dataframes(gmp_df, subs_df):
    """Merge GMP and subscription dataframes on IPO name."""
    gmp_df['Merge_key'] = gmp_df['Name▲▼'].str.split().str[0].str.lower()
    subs_df['Merge_key'] = subs_df['IPO Name'].str.split().str[0].str.lower()

    merged = gmp_df.merge(subs_df, on='Merge_key', how='left')
    return merged[['IPO Name', 'GMP▲▼', 'Price (₹)▲▼', 'Lot▲▼', 'Close▲▼',
                   'Type', 'QIB', 'NII / HNI', 'Retail']]


def collect_and_merge():
    """Scrape both URLs, merge data, and save JSON output."""
    try:
        date_column = 'Close▲▼'
        upcoming_ipos = scrape_url(urls[0], 0)
        if upcoming_ipos is None:
            logging.error("Upcoming IPOs table not found")
            sys.exit(1)

        upcoming_ipos[date_column] = upcoming_ipos[date_column].apply(modify_ipo_date)
        today = date.today()
        upcoming_ipos = upcoming_ipos[upcoming_ipos[date_column].dt.date >= today].copy()

        raw_df = scrape_url(urls[1], 1)
        if raw_df is None:
            logging.error("Subscription status table not found")
            sys.exit(1)

        headers = raw_df.iloc[0]
        data_df = raw_df.iloc[1:].reset_index(drop=True)
        data_df.columns = headers

        merged_df = merge_dataframes(upcoming_ipos, data_df)

        column_mapping = {
            'IPO Name': 'Name',
            'GMP▲▼': 'GMP',
            'Close▲▼': 'Close_date',
            'Listing▲▼': 'Listing_date',
            'Price (₹)▲▼': 'Price',
            'IPO Size (₹ in cr)▲▼': 'Ipo_size',
            'Lot▲▼': 'Lot_size',
            'NII / HNI': 'NII'
        }

        merged_df = merged_df.rename(columns=column_mapping)
        merged_df['Close_date'] = merged_df['Close_date'].dt.strftime('%d-%b-%Y')

        output_path = "./ipo_dashboard.json"
        merged_df.to_json(output_path, orient='records', indent=2)
        logging.info(f"Data successfully written to {output_path}")

    except Exception as e:
        logging.exception("collect_and_merge failed")
        sys.exit(1)


if __name__ == "__main__":
    collect_and_merge()
