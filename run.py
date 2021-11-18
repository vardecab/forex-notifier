# ==================================== #
#            forex-notifier            #
# ==================================== #

# ------------ import libs ----------- #

import requests # access API URL 
import time # calculate script's run time

# --------- start + run time --------- #

start_time = time.time() # run time start
print("Starting the script...")

# --------- let the fun begin -------- #

# build URL
API_url = 'https://free.currconv.com/api/v7/convert' # API URL 
API_key = open("API_key.txt", "r").read() # read API key from file
compact = '&compact=y' # compact response from API

# USD <> PLN
currency_pair = 'USD_PLN' # currency pair
get_data = requests.get(url=API_url + API_key + '&q=' + currency_pair + compact).json()
rate = round(get_data[currency_pair]['val'],2) # currency pair rate rounded to 2 decimals
print(rate)

# EUR <> PLN
currency_pair = 'EUR_PLN' # currency pair
get_data = requests.get(url=API_url + API_key + '&q=' + currency_pair + compact).json()
rate = round(get_data[currency_pair]['val'],2) # currency pair rate rounded to 2 decimals
print(rate)

# GBP <> PLN
currency_pair = 'GBP_PLN' # currency pair
get_data = requests.get(url=API_url + API_key + '&q=' + currency_pair + compact).json()
rate = round(get_data[currency_pair]['val'],2) # currency pair rate rounded to 2 decimals
print(rate)

# ------------- run time ------------- #

end_time = time.time() # run time end 
total_run_time = round(end_time-start_time,2)
print(f"Total script run time: {total_run_time} seconds.")