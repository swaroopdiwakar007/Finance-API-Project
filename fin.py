
import requests 
from bs4 import BeautifulSoup 
from constants import *
import pandas as pd
import datetime
import time

def initialize():
    global stocks
    URL = URL.replace('stock_exchange', STOCK_EXCHANGE)
    df = pd.read_excel('nse_list.xlsx', sheet_name=0) # can also index sheet by name or fetch all sheets
    stocks = df['Symbol'].tolist()
    while str(stocks[-1]) == 'nan':
        stocks.pop()

def get_value(tag, dict2):
    val = soup.find_all(tag, dict2)[0].contents[0].replace(',','')
    return val


def form_dict(stock):
    try:
        DICT1["PREV VAL"] = get_value("td", {"data-test": "PREV_CLOSE-value"})
        DICT1["OPEN VAL"] = get_value("td", {"data-test": "OPEN-value"})
        DICT1["CURR VAL"] = get_value("fin-streamer", {"data-field": "regularMarketPrice", "data-symbol":f"{stock}.NS"})
        DICT1["BETA VAL"] = get_value("td", {"data-test": "BETA_5Y-value"})
        DICT1["PE RATIO"] = get_value("td", {"data-test": "PE_RATIO-value"})
        DICT1["EPS RATIO"] = get_value("td", {"data-test": "EPS_RATIO-value"})
    except:
        return DICT1

def get_current_stock_data(stock):
    global soup
    headers = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate, br",
        "Connection":"keep-alive",
        "User-Agent":"PostmanRuntime/7.32.3"
    }
    params = {'p':f'{stock}.NS'}
    max_count = MAX_COUNT
    r = requests.get(URL.replace('nse_stock_symbol', stock), timeout=10, headers=headers, params=params) 
    while r.status_code != 200 and max_count != 0:
        r = requests.get(URL.replace('nse_stock_symbol', stock), timeout=10, headers=headers, params=params) 
        max_count -= 1
        time.sleep(1)
    soup = BeautifulSoup(r.content, 'html5lib')

def save_csv_file(str1):
    file = open(f"{datetime.datetime.now():%Y_%m_%d}.csv", 'w')
    file.write(str1)
    file.close()

def get_stock_val():
    global str1
    str1 = 'COMPANY,'+','.join(DICT1.keys())
    initialize()
    for stock in stocks:
        get_current_stock_data(stock)
        form_dict(stock)
        str1 += f'\n{stock},{",".join([DICT1[val] for val in DICT1.keys()])}'
    
    save_csv_file(str1)

get_stock_val()
