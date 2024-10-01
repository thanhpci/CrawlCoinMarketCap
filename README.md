
# CoinMarketCap Historical Snapshot Crawler

## Description
This project is used to crawl historical snapshot data from CoinMarketCap on **June 27, 2021**. The crawler retrieves market cap data and saves it into a CSV file.

Website to be crawled:
https://coinmarketcap.com/historical/20210627/

The data will be saved into a CSV file with the following columns:
- rank: Rank of the coin
- name: Name of the coin
- symbol: Symbol of the coin
- market_cap: Market capitalization of the coin
- price: Price of the coin
- circulating_supply: Circulating supply of the coin
- volume: Trading volume
- change_7d: 7-day percentage change

## Installation Guide

### 1. Install ChromeDriver:
Download the appropriate version of ChromeDriver that matches your Chrome version.
After downloading, place the ChromeDriver file in the following path:
```
C:/Program Files/Google/Chrome/Application/chromedriver.exe
```

### 2. Install dependencies from requirements.txt:
To install the required packages, run the following commands using Miniconda:

```bash
conda create --name crawl_coin python=3.8
conda activate crawl_coin
pip install -r requirements.txt
```

### 3. Run the crawler:
To run the program, simply type the following command:

```bash
python CrawlCoinMarketCap.py
```

## Output:
The data will be saved in CSV format with the column structure as described above. The CSV file will be saved in the `data` directory at the root of the project.

Example:
```
rank,name,symbol,market_cap,price,circulating_supply,volume,change_7d
1,Bitcoin,BTC,$649,461,677,014.11,$34,649.64,18,743,675 BTC,$35,511,640,893.97,-2.94%
2,Ethereum,ETH,$264,691,370,246.21,$2,295.24,115,008,345 ETH,$24,158,123,467.58,1.58%
```

## Data Directory:
The data will be stored in the `data` directory at the root of the project, with the filename in the format `YYYYMMDD.csv`. For example:

```
project-root/
    CrawlCoinMarketCap.py
    requirements.txt
    data/
        20210627.csv
```
