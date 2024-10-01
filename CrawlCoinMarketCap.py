from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
import csv
import os

import logging
import os

log_file_path = os.path.join(os.getcwd(), 'coin_scraper.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def scroll_slowly_to_top(driver, step=100, delay=0.1):
    current_position = driver.execute_script("return window.pageYOffset;")
    while current_position > 0:
        current_position = max(current_position - step, 0)
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        sleep(delay)

    driver.execute_script("window.scrollTo(0, 0);")
    sleep(0.5)
    logging.info("Slowly scrolled to the top of the page")


def scroll_slowly_to_bottom(driver, step=100, delay=0.1):
    current_position = driver.execute_script("return window.pageYOffset;")
    max_height = driver.execute_script("return document.body.scrollHeight;")
    while current_position < max_height:
        current_position = min(current_position + step, max_height)
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        sleep(delay)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(0.5)
    logging.info("Slowly scrolled to the bottom of the page")


def measure_table_components(driver):
    first_row = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table tbody tr.cmc-table-row'))
    )

    row_height = first_row.size['height']
    distance_to_first_row = first_row.location['y']

    scroll_slowly_to_bottom(driver)
    last_row = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr.cmc-table-row')[-1]
    total_height = driver.execute_script("return document.body.scrollHeight")
    last_row_bottom = last_row.location['y'] + last_row.size['height']
    distance_from_bottom = total_height - last_row_bottom

    return distance_to_first_row, row_height, distance_from_bottom
def calculate_scroll_position(distance_to_first_row, row_height, num_rows):
    return distance_to_first_row + (row_height * (num_rows - 1))
def scroll_from_current_to_row(driver, distance_to_first_row, row_height, target_row, step=100, delay=0.1):
    current_position = driver.execute_script("return window.pageYOffset;")
    target_position = calculate_scroll_position(distance_to_first_row, row_height, target_row)

    window_height = driver.execute_script("return window.innerHeight;")
    middle_offset = window_height / 2 - row_height / 2
    target_position -= middle_offset

    if current_position < target_position:
        while current_position < target_position:
            current_position = min(current_position + step, target_position)
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            sleep(delay)
    else:
        while current_position > target_position:
            current_position = max(current_position - step, target_position)
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            sleep(delay)

    driver.execute_script(f"window.scrollTo(0, {target_position});")
    sleep(0.5)

    logging.info(f"Scrolled to row {target_row}")
def scroll_from_bottom_to_row(driver, distance_to_first_row, row_height, target_row, step=100, delay=0.1):
    scroll_slowly_to_bottom(driver)
    sleep(1)
    scroll_from_current_to_row(driver, distance_to_first_row, row_height, target_row)
    logging.info(f"Scrolled from bottom to row {target_row}")
def scroll_from_top_to_row(driver, distance_to_first_row, row_height, target_row, step=100, delay=0.1):
    scroll_slowly_to_top(driver)
    sleep(1)
    scroll_from_current_to_row(driver, distance_to_first_row, row_height, target_row, step, delay)
    logging.info(f"Scrolled from top to row {target_row}")
def read_coin_data(coin):
    try:
        rank = coin.find_element(By.CSS_SELECTOR, 'td:nth-child(1) div').text.strip()
        name = coin.find_element(By.CSS_SELECTOR, 'td:nth-child(2) div a:last-child').text.strip()
        symbol = coin.find_element(By.CSS_SELECTOR, 'td:nth-child(3) div').text.strip()

        try:
            market_cap = coin.find_element(By.CSS_SELECTOR, 'td:nth-child(4) div').text.strip()
        except Exception:
            market_cap = "--"

        try:
            price = coin.find_element(By.CSS_SELECTOR, 'td:nth-child(5) div').text.strip()
        except Exception:
            price = "--"

        try:
            circulating_supply = coin.find_element(By.CSS_SELECTOR, 'td:nth-child(6) div').text.strip()
        except Exception:
            circulating_supply = "--"

        try:
            volume = coin.find_element(By.CSS_SELECTOR, 'td:nth-child(7) a:last-child').text.strip()
        except Exception:
            volume = "--"

        try:
            change_7d = coin.find_element(By.CSS_SELECTOR, 'td:nth-child(10) div').text.strip()
        except Exception:
            change_7d = "--"

        return {
            'rank': rank,
            'name': name,
            'symbol': symbol,
            'market_cap': market_cap,
            'price': price,
            'circulating_supply': circulating_supply,
            'volume': volume,
            'change_7d': change_7d
        }
    except NoSuchElementException:
        return None
def scroll_for_waiting():
    scroll_from_current_to_row(browser, distance_to_first_row, row_height, start_row)
    scroll_from_current_to_row(browser, distance_to_first_row, row_height, end_row)
    sleep(2)
    scroll_from_current_to_row(browser, distance_to_first_row, row_height, start_row)
    scroll_from_current_to_row(browser, distance_to_first_row, row_height, end_row)
    sleep(2)

def dump_to_file(coin_data, file_path):
    max_rank_in_csv = 0
    if os.path.exists(file_path):
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            if rows:
                max_rank_in_csv = int(rows[-1]['rank'])

    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['rank', 'name', 'symbol', 'market_cap', 'price', 'circulating_supply', 'volume', 'change_7d']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if max_rank_in_csv == 0:
            writer.writeheader()

        for rank in sorted(coin_data.keys(), key=int):
            if int(rank) > max_rank_in_csv:
                writer.writerow(coin_data[rank])
def process_coin(coin, current_rank, missing_coins, coin_data):
    coin_info = read_coin_data(coin)
    if coin_info:
        rank = coin_info['rank']
        if rank in missing_coins:
            missing_coins.remove(rank)
        coin_data[rank] = coin_info
        logging.info(f"Read: Rank: {rank}, Name: {coin_info['name']}")
    else:
        missing_coins.add(str(current_rank))

    return missing_coins, coin_data
def click_load_more(driver):
    try:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.cmc-table-listing__loadmore button'))
        )
        load_more_button.click()
        logging.info("Clicked 'Load More'")
        sleep(2)
        return True
    except (NoSuchElementException, TimeoutException):
        logging.warning("'Load More' button not found")
        return False

def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_file_path(root, year, month, date):
    return f"{root}/{year}{month:02d}{date:02d}.csv"


if __name__ == "__main__":
    logging.info("Starting coin scraping process")
    date = 27
    month = 6
    year = 2021
    url = f"https://coinmarketcap.com/historical/{year}{month:02d}{date:02d}/"

    file_path = get_file_path("data", year, month, date)
    ensure_directory_exists(file_path)

    browser = webdriver.Chrome(executable_path="C:/Program Files/Google/Chrome/Application/chromedriver.exe")
    browser.get(url)


    sleep(3)
    distance_to_first_row, row_height, distance_from_bottom_to_end_row = measure_table_components(browser)
    scroll_slowly_to_top(browser)

    coin_data = {}
    missing_coins = set()
    coins_per_load = 200

    while True:
        coins = browser.find_elements(By.CSS_SELECTOR, 'tr.cmc-table-row')
        total_coins = len(coins)

        start_row = len(coin_data) + 1
        end_row = total_coins

        logging.info(f"Loading data from row {start_row} to row {end_row}")
        scroll_for_waiting()

        coins = browser.find_elements(By.CSS_SELECTOR, 'tr.cmc-table-row')

        for i in range(start_row, end_row + 1):
            missing_coins, coin_data = process_coin(coins[i - 1], i, missing_coins, coin_data)

        while missing_coins:
            dump_to_file(coin_data, "coin_data.csv")

            position = missing_coins.pop()
            missing_coins.add(position)

            scroll_from_current_to_row(browser, distance_to_first_row, row_height, int(position))
            coins = browser.find_elements(By.CSS_SELECTOR, 'tr.cmc-table-row')

            for rank in list(missing_coins):
                coin = coins[int(rank) - 1]
                missing_coins, coin_data = process_coin(coin, rank, missing_coins, coin_data)

        dump_to_file(coin_data, file_path)

        click_load_more(browser)
