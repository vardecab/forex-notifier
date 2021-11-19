# ==================================== #
#            forex-notifier            #
# ==================================== #

# ------------ import libs ----------- #

import requests # access API URL 
import time # calculate script's run time
# notifications ↓ 
from sys import platform # check platform (Windows/macOS)
if platform == 'win32':
    from win10toast_click import ToastNotifier # Windows 10/11 notifications
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
compact = '&compact=y' # get "compact" response from API - ain't need no fluff

# --------- let the fun begin -------- #

def getRates(currency, base_currency): 

    currency = currency.upper() # must be in uppercase for API call
    base_currency = base_currency.upper() # must be in uppercase for API call
    
    try:
        previous_rate = float(open("./comparison_files/" + currency + ".txt", "r").read()) # read previous rate
        # print(f'Previous rate loaded.') # status
    except FileNotFoundError: # file doesn't exist
        #* NOTE: File doesn't exist, 1) first launch or 2) there was a problem with saving the value last time the script ran. 
        pass # let's move on 

    currency_pair = currency + "_" + base_currency # desired currency + base_currency
    get_data = requests.get(url=API_url + API_key + '&q=' + currency_pair + compact).json() # get data from API
    rate = round(get_data[currency_pair]['val'],2) # currency pair rate rounded to 2 decimals
    
    try:
        if previous_rate < rate:
            change_symbol = '⬆️'
        elif previous_rate == rate: 
            change_symbol = '↔️'
        else: 
            change_symbol = '⬇️'
        print(f'{currency}: {rate} {change_symbol} ({previous_rate})')
    except NameError: # variable doesn't exist
        #* NOTE: Variable doesn't exist, either 1) first launch or 2) there was a problem with saving the value last time the script ran.
        pass # let's move on

    with open("./comparison_files/" + currency + ".txt", "w") as file: # save current rate for comparison in the next run
        file.write(str(rate))
        # print(f'File {file} saved.') # status
        
    return [rate, change_symbol, previous_rate] # return a list with values to be used in notification 
    #* NOTE: 1/2: eg. get_currency1[0] => rate; get_currency1[1] => change_symbol; get_currency1[2] => previous_rate 
    
# ----- put your currencies here ----- #

base_currency = 'pln'

currency1 = 'usd'
currency2 = 'eur'
currency3 = 'gbp'

# ----- run function to get rates ---- #

get_currency1 = getRates(currency1, base_currency)
get_currency2 = getRates(currency2, base_currency)
get_currency3 = getRates(currency3, base_currency)

# ----------- notifications ---------- #

try:
    if platform == "darwin": # macOS
        #* NOTE: 2/2
        pync.notify(f'{currency1.upper()}: {get_currency1[0]} {get_currency1[1]} ({get_currency1[2]})\n{currency2.upper()}: {get_currency2[0]} {get_currency2[1]} ({get_currency2[2]})\n{currency3.upper()}: {get_currency3[0]} {get_currency3[1]} ({get_currency3[2]})', title='Forex update:', contentImage="https://cdn-icons-png.flaticon.com/512/4646/4646154.png", sound="Funk")
    elif platform == "win32": # Windows
        # TODO: check if it works 
        toaster.show_toast(title="Forex update", msg=f'{currency1.upper()}: {get_currency1[0]} {get_currency1[1]} ({get_currency1[2]})\n{currency2.upper()}: {get_currency2[0]} {get_currency2[1]} ({get_currency2[2]})\n{currency3.upper()}: {get_currency2[0]} {get_currency2[1]} ({get_currency2[2]})', icon_path="", duration=None, threaded=True) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
except NameError: # variable doesn't exist because file doesn't exist
    #* NOTE: First launch or there was a problem with saving the value.
    pass

# ------------- run time ------------- #

end_time = time.time() # run time end 
total_run_time = round(end_time-start_time,2)
print(f"Total script run time: {total_run_time} seconds.")