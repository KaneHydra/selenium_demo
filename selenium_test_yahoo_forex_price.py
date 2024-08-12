# -*- coding=utf-8 -*-
import numpy as np
import pandas as pd
import polars as pl
from rich import print
from datetime import datetime
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Set the configuration to display all rows
pl.Config.set_tbl_rows(-1)


def convert_to_datetime(date_str):
    current_year = datetime.now().year
    return datetime.strptime(
        f"{current_year} {date_str}", "%Y %m/%d %H:%M"
    )  # .strftime("%Y-%m-%d %H:%M")


chromedriver_path: str = "./chromedriver-win64/chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--headless=new")  # for Chrome >= 109
chrome_options.add_argument("--no-sandbox")
chrome_services = webdriver.ChromeService(executable_path=chromedriver_path)
chrome_options.binary_location = "./chrome-win64/chrome.exe"
# Initialize the WebDriver
with webdriver.Chrome(options=chrome_options, service=chrome_services) as driver:
    # Open the target URL
    url = "https://tw.stock.yahoo.com/currency-converter/"
    driver.get(url)
    # data_elements = driver.find_elements(By.CSS_SELECTOR, "li[class*='List(n)']")

    # Wait for the AJAX content to load
    header_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class^="table-header "]'))
    )
    body_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class^="table-body "]'))
    )

    # Extract header and body content
    headers = [
        header.text
        for header in header_element.find_elements(
            By.CSS_SELECTOR, 'div[class*="Ta(start)"]'
        )
    ]
    headers.extend(
        [
            header.text
            for header in header_element.find_elements(
                By.CSS_SELECTOR, 'div[class*="Ta(end)"]'
            )
        ]
    )
    headers.append("銀行網址")

    data = []
    rows = body_element.find_elements(By.CSS_SELECTOR, 'li[class*="List(n)"]')
    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, 'div[class*="Fxg(1)"]')
        row_data = [
            cell.text
            for cell in row.find_elements(By.CSS_SELECTOR, 'div[class*="Ta(start)"]')
        ]
        row_data.extend([cell.text for cell in cells])
        bank_url = "https://tw.stock.yahoo.com" + row.find_element(
            By.TAG_NAME, "a"
        ).get_dom_attribute("href")
        row_data.append(bank_url)
        data.append(row_data)

    # Convert to pandas DataFrame
    df = pd.DataFrame(data, columns=headers)
    # Replace '-' with NaN
    df.replace("-", np.nan, inplace=True)
    # Convert specified columns to float
    columns_to_convert = ["即期買入", "即期賣出", "現金買入", "現金賣出"]
    df[columns_to_convert] = df[columns_to_convert].astype(float)
    # Convert datetime format
    df["資料時間"] = df["資料時間"].apply(convert_to_datetime)
    # display pandas dataframe
    print("\npandas table:")
    print(df)

    # Create a Polars DataFrame
    pl_df = pl.DataFrame(data, schema=headers, orient="row")

    # Replace '-' with None (Polars treats None as NaN)
    pl_df = pl_df.with_columns(
        [
            pl.when(pl.col(col) == "-").then(None).otherwise(pl.col(col)).alias(col)
            for col in pl_df.columns
        ]
    )
    # Convert specified columns to float
    columns_to_convert = ["即期買入", "即期賣出", "現金買入", "現金賣出"]
    pl_df = pl_df.with_columns(
        [pl.col(col).cast(pl.Float64) for col in columns_to_convert]
    )
    # Convert datetime format
    pl_df = pl_df.with_columns(
        pl.col("資料時間")
        .map_elements(convert_to_datetime, return_dtype=pl.Datetime)
        .alias("資料時間")
    )
    # display polars dataframe
    print("\npolars table:")
    print(pl_df)

    # Pretty print the DataFrame with grid border
    print("\ntabulate table:")
    print(tabulate(df, headers="keys", tablefmt="grid"))

    last_update_time = df["資料時間"].max().strftime("%Y-%m-%d_%H-%M")

    df.to_csv(f"./data/currency-price_{last_update_time}.csv", header=True, index=False)
