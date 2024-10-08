#!/usr/bin/env python

import os
import time
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options
options = Options()
download_dir = os.path.abspath("downloads")  # Replace with your desired path
os.makedirs(download_dir, exist_ok=True)

options.add_argument("--headless")  # Enable headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")

# Configure Chrome preferences
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "profile.default_content_settings.popups": 0,
    "profile.default_content_setting_values.automatic_downloads": 1,
    "safebrowsing.enabled": True,
    "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
    "profile.default_content_setting_values.notifications": 1,
    "download.extensions_to_open": "applications/csv,text/csv,application/vnd.ms-excel",
}
options.add_experimental_option("prefs", prefs)

# Initialize the driver
driver = webdriver.Chrome(options=options)

try:
    driver.get(
        "https://www.bog.gov.gh/treasury-and-the-markets/daily-interbank-fx-rates/"
    )

    # Wait and click the 'Export' button
    export_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Export')]"))
    )
    export_button.click()
    print("Clicked the 'Export' button.")

    # Wait and click the 'CSV' button
    csv_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@class,'buttons-csv') and contains(.,'CSV')]")
        )
    )
    csv_button.click()
    print("Clicked the 'CSV' button.")

    # Wait for the file to be downloaded
    timeout = 40  # Adjust as necessary
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(download_dir):
            if fname.endswith(".crdownload"):
                dl_wait = True
        seconds += 1

    if not dl_wait:
        print("File downloaded successfully.")

        # Get list of downloaded files matching *.csv
        list_of_files = glob.glob(os.path.join(download_dir, "*.csv"))
        if list_of_files:
            # Get the most recent file
            latest_file = max(list_of_files, key=os.path.getctime)

            # Get current timestamp
            timestamp = time.strftime("%Y%m%d%H%M%S")

            # Build new file name with timestamp
            base_name = os.path.basename(latest_file)
            new_file_name = f"{os.path.splitext(base_name)[0]}_{timestamp}.csv"
            new_file_path = os.path.join(download_dir, new_file_name)

            # Rename the file
            os.rename(latest_file, new_file_path)

            print(f"File renamed to: {new_file_name}")
        else:
            print("No CSV files found in the download directory.")

    else:
        print("Download timed out.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()