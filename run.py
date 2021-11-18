# ==================================== #
#            forex-notifier            #
# ==================================== #

# ------------ import libs ----------- #

import requests # access API URL 
import time # calculate script's run time
# notifications ↓ 
from sys import platform # check platform (Windows/macOS)
if platform == 'win32':
    from win10toast_click import ToastNotifier # Windows 10 notifications
    toaster = ToastNotifier() # initialize win10toast
elif platform == 'darwin':
    import pync # macOS notifications

# --------- start + run time --------- #

start_time = time.time() # run time start
print("Starting the script...")

# ------------- build URL ------------ #

API_url = 'https://free.currconv.com/api/v7/convert' # API URL 
API_key = open("API_key.txt", "r").read() # read API key from file
API_key = '?apiKey='+API_key # join URL parameter with value
compact = '&compact=y' # compact response from API

# --------- let the fun begin -------- #

# TODO: there should be a function to decrease SLOC, lots of repeated code

# USD <> PLN

try:
    previous_usd = float(open("./comparison_files/usd.txt", "r").read()) # read previous rate
except FileNotFoundError: # file doesn't exist
    #* NOTE: File doesn't exist, first launch or there was a problem with saving the value.
    pass

currency_pair1 = 'USD_PLN' # currency pair
get_data = requests.get(url=API_url + API_key + '&q=' + currency_pair1 + compact).json() # get data from API
rate_usd = round(get_data[currency_pair1]['val'],2) # currency pair rate rounded to 2 decimals

try:
    if previous_usd < rate_usd:
        change_symbol_usd = '⬆️'
    elif previous_usd == rate_usd: 
        change_symbol_usd = '↔️'
    else: 
        change_symbol_usd = '⬇️'
    print(f'USD: {rate_usd} {change_symbol_usd} ({previous_usd})')
except NameError: # variable doesn't exist because file doesn't exist
    #* NOTE: First launch or there was a problem with saving the value.
    pass

with open('./comparison_files/usd.txt', 'w') as file_usd: # save current rate for comparison in the next run
    file_usd.write(str(rate_usd))

# EUR <> PLN

try:
    previous_eur = float(open("./comparison_files/eur.txt", "r").read()) # read previous rate
except FileNotFoundError: # file doesn't exist
    #* NOTE: File doesn't exist, first launch or there was a problem with saving the value.
    pass

currency_pair2 = 'EUR_PLN' # currency pair
get_data = requests.get(url=API_url + API_key + '&q=' + currency_pair2 + compact).json() # get data from API
rate_eur = round(get_data[currency_pair2]['val'],2) # currency pair rate rounded to 2 decimals

try:    
    if previous_eur < rate_eur:
        change_symbol_eur = '⬆️'
    elif previous_eur == rate_eur: 
        change_symbol_eur = '↔️'
    else: 
        change_symbol_eur = '⬇️'
    print(f'EUR: {rate_eur} {change_symbol_eur} ({previous_eur})')
except NameError: # variable doesn't exist because file doesn't exist
    #* NOTE: First launch or there was a problem with saving the value.
    pass

with open('./comparison_files/eur.txt', 'w') as file_eur: # save current rate for comparison in the next run
    file_eur.write(str(rate_eur))

# GBP <> PLN

try:
    previous_gbp = float(open("./comparison_files/gbp.txt", "r").read()) # read previous rate
except FileNotFoundError: # file doesn't exist
    #* NOTE: File doesn't exist, first launch or there was a problem with saving the value.
    pass

currency_pair3 = 'GBP_PLN' # currency pair
get_data = requests.get(url=API_url + API_key + '&q=' + currency_pair3 + compact).json() # get data from API
rate_gbp = round(get_data[currency_pair3]['val'],2) # currency pair rate rounded to 2 decimals

try:
    if previous_gbp < rate_gbp:
        change_symbol_gbp = '⬆️'
    elif previous_gbp == rate_gbp: 
        change_symbol_gbp = '↔️'
    else: 
        change_symbol_gbp = '⬇️'
    print(f'GBP: {rate_gbp} {change_symbol_gbp} ({previous_gbp})')
except NameError: # variable doesn't exist because file doesn't exist
    #* NOTE: First launch or there was a problem with saving the value.
    pass

with open('./comparison_files/gbp.txt', 'w') as file_gbp: # save current rate for comparison in the next run
    file_gbp.write(str(rate_gbp))

# ----------- notifications ---------- #

try:
    if platform == "darwin": # macOS
        pync.notify(f'USD: {rate_usd} {change_symbol_usd} ({previous_usd})\nEUR: {rate_eur} {change_symbol_eur} ({previous_eur})\nGBP: {rate_gbp} {change_symbol_gbp} ({previous_gbp})', title='Forex update:', contentImage="https://cdn-icons-png.flaticon.com/512/4646/4646154.png", sound="Funk")
    elif platform == "win32": # Windows
        # TODO: check if it works 
        toaster.show_toast(title="Forex update", msg=f'{currency_pair1}: {rate_usd}\n{currency_pair2}: {rate_eur}\n{currency_pair3}: {rate_gbp}', icon_path="", duration=None, threaded=True) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
except NameError: # variable doesn't exist because file doesn't exist
    #* NOTE: First launch or there was a problem with saving the value.
    pass

# ------------- run time ------------- #

end_time = time.time() # run time end 
total_run_time = round(end_time-start_time,2)
print(f"Total script run time: {total_run_time} seconds.")