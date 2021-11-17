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

# read API key
API_key = open("API_key.txt", "r").read()

# USD <> PLN
get_data = requests.get(url='https://free.currconv.com/api/v7/convert?apiKey=' + API_key + '&q=USD_PLN&compact=y')
print(get_data.json())

# EUR <> PLN
get_data = requests.get(url='https://free.currconv.com/api/v7/convert?apiKey=' + API_key + '&q=EUR_PLN&compact=y')
print(get_data.json())

# GBP <> PLN
get_data = requests.get(url='https://free.currconv.com/api/v7/convert?apiKey=' + API_key + '&q=GBP_PLN&compact=y')
print(get_data.json())

# ------------- run time ------------- #

end_time = time.time() # run time end 
total_run_time = round(end_time-start_time,2)
print(f"Total script run time: {total_run_time} seconds.")