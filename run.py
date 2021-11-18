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

# --------- let the fun begin -------- #

# build URL
API_url = 'https://free.currconv.com/api/v7/convert' # API URL 
API_key = open("API_key.txt", "r").read() # read API key from file
compact = '&compact=y' # compact response from API

# USD <> PLN
currency_pair1 = 'USD_PLN' # currency pair
get_data = requests.get(url=API_url + API_key + '&q=' + currency_pair1 + compact).json()
rate1 = round(get_data[currency_pair1]['val'],2) # currency pair rate rounded to 2 decimals
print(f'{currency_pair1}: {rate1}')

# EUR <> PLN
currency_pair2 = 'EUR_PLN' # currency pair
get_data = requests.get(url=API_url + API_key + '&q=' + currency_pair2 + compact).json()
rate2 = round(get_data[currency_pair2]['val'],2) # currency pair rate rounded to 2 decimals
print(f'{currency_pair2}: {rate2}')

# GBP <> PLN
currency_pair3 = 'GBP_PLN' # currency pair
get_data = requests.get(url=API_url + API_key + '&q=' + currency_pair3 + compact).json()
rate3 = round(get_data[currency_pair3]['val'],2) # currency pair rate rounded to 2 decimals
print(f'{currency_pair3}: {rate3}')

# ----------- notifications ---------- #

if platform == "darwin":
    pync.notify(f'{currency_pair1}: {rate1}\n{currency_pair2}: {rate2}\n{currency_pair3}: {rate3}', title='Forex update:',
                contentImage="https://cdn-icons-png.flaticon.com/512/4646/4646154.png", sound="Funk")
elif platform == "win32":
    # TODO: check if it works 
    toaster.show_toast(title="Forex update", msg=f'{currency_pair1}: {rate1}\n{currency_pair2}: {rate2}\n{currency_pair3}: {rate3}', icon_path="", duration=None, threaded=True) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active

# ------------- run time ------------- #

end_time = time.time() # run time end 
total_run_time = round(end_time-start_time,2)
print(f"Total script run time: {total_run_time} seconds.")