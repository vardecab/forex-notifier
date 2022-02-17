# ==================================== #
#            forex-notifier            #
# ==================================== #

# ------------ import libs ----------- #

import time # calculate script's run time
import sys # terminate script
import requests # send data via webhook to IFTTT

# notifications ↓ 
from sys import platform # check platform (Windows/macOS)
if platform == 'darwin':
    import pync # macOS notifications
elif platform == 'win32':
    from win10toast_click import ToastNotifier # Windows 10/11 notifications
    toaster = ToastNotifier() # initialize win10toast
import webbrowser # open URLs from notification

# import alert thresholds
import alertThresholds # import local file

# --------- start + run time --------- #

start_time = time.time() # run time start
print("Starting the script...") # status

# ------------- build URL ------------ #

API_url = 'https://free.currconv.com/api/v7/convert' # API URL 
try: 
    API_key = open("./api/TFCC_API-key.txt", "r").read() # read API key from file
except FileNotFoundError: 
    print("Couldn't find The Free Currency Converter API key. Add file to the folder / check file name.")
    print("Closing...")
    sys.exit() # terminate script

API_key = f'?apiKey={API_key}'
compact = '&compact=y' # get "compact" response from API - ain't need no fluff

# --------- let the fun begin -------- #

def getRates(currency, base_currency): 

    currency = currency.upper() # must be in uppercase for API call
    base_currency = base_currency.upper() # must be in uppercase for API call
    
    # --------- get previous rate -------- #
    
    try:
        previous_rate = float(open("./comparison_files/" + currency + ".txt", "r").read()) # read previous rate
        # print(f'Previous rate loaded.') # status
    except FileNotFoundError: # file doesn't exist
        # NOTE: File doesn't exist, 1) first launch or 2) there was a problem with saving the value last time the script ran. 
        pass # let's move on 

    # --------- get current rate --------- #
    
    currency_pair = currency + "_" + base_currency # desired currency + base_currency
    print(currency_pair)
    
    try:
        buildURL = API_url + API_key + '&q=' + currency_pair + compact
        print(buildURL) # debug
        get_data = requests.get(url=buildURL).json() # get data from API
        rate = round(get_data[currency_pair]['val'],2) # take value from JSON returned from API and round to 2 decimals
    except:
        # NOTE: Possible 5## error / API down.
        print("Can't access API — check your Internet connection and API Server Status: https://free.currencyconverterapi.com. Closing...")
        sys.exit()
        
    # --------------- trend -------------- #

    trend = 0 # based on trend decide which icon to use in notification 

    # show symbols
    try:
        if previous_rate < rate:
            if platform == 'darwin':
                change_symbol = '⬆️' # emoji
            elif platform == 'win32':
                change_symbol = ">" # Windows neither does display emojis well nor ↑ ↓ in a toast notification 
            trend += 1
        elif previous_rate == rate: 
            if platform == 'darwin':
                change_symbol = "↔️" # emoji
            elif platform == 'win32':
                change_symbol = '=' # Windows neither does display emojis well nor ↑ ↓ in a toast notification 
        else: 
            if platform == 'darwin':
                change_symbol = '⬇️' # emoji
            elif platform == 'win32':
                change_symbol = "<" # Windows neither does display emojis well nor ↑ ↓ in a toast notification 
            trend -= 1
        print(f'{currency}: {rate:.2f} {change_symbol} ({previous_rate:.2f})') # :.2f used to always show 2 decimals
    except NameError: # variable doesn't exist
    #     # NOTE: Variable doesn't exist, either 1) first launch or 2) there was a problem with saving the value last time the script ran.
        pass # let's move on

    # ---- save current rate for later --- #

    with open("./comparison_files/" + currency + ".txt", "w") as file: # save current rate for comparison in the next run
        file.write(str((f'{rate:.2f}')))
        print(f'File with {currency} saved.') # status

    # ----------- return values ---------- #

    return [rate, change_symbol, previous_rate, trend] # return a list with values to be used in notification
    # NOTE: 1/2: eg. get_currency1[0] => rate; get_currency1[1] => change_symbol; get_currency1[2] => previous_rate, etc.
    
# ----- put your currencies here ----- #

base_currency = 'pln'

currency1 = 'usd'
currency2 = 'eur'
currency3 = 'gbp'
currency4 = 'btc'

# ----- run function to get rates ---- #

get_currency1 = getRates(currency1, base_currency)
get_currency2 = getRates(currency2, base_currency)
get_currency3 = getRates(currency3, base_currency)
get_currency4 = getRates(currency4, 'usd') # BTC <> USD

# ---- IFTTT automation for alerts --- #

try: 
    ifttt_maker_key = open('./api/IFTTT-key.txt', 'r').read() # read API key
except FileNotFoundError:
    print("Couldn't find IFTTT API key. Add file to the folder / check file name.")
    print("Closing...") # status
    sys.exit() # terminate script
    # TODO: maybe pass instead? Not everyone has to have IFTTT.

event_name = 'forex' 
webhook_url = f'https://maker.ifttt.com/trigger/{event_name}/with/key/{ifttt_maker_key}' # build URL

def send_to_IFTTT(currency, rate, message):
    
    # data passed to IFTTT ↓
    currency = currency.upper() # nice and tidy
    report = {
        "value1": currency,
        "value2": rate,
        "value3": message # additional message 
    }
    requests.post(webhook_url, data=report) # send data to IFTTT
    print("Alert sent to IFTTT.") # status

# ----------- custom alert ----------- #

# USD
if get_currency1[0] <= float(alertThresholds.alertUSD_buy):
    message = 'kup'
    send_to_IFTTT(currency1, get_currency1[0], message)
    print(f'{currency1.upper()}: {get_currency1[0]} // BUY!!!')
elif get_currency1[0] >= float(alertThresholds.alertUSD_sell):
    message = 'sprzedaj'
    send_to_IFTTT(currency1, get_currency1[0], message)
    print(f'{currency1.upper()}: {get_currency1[0]} // SELL!!!')
    
# EUR
if get_currency2[0] <= float(alertThresholds.alertEUR_buy):
    message = 'kup'
    send_to_IFTTT(currency2, get_currency2[0], message)
    print(f'{currency2.upper()}: {get_currency2[0]} // BUY!!!')
elif get_currency2[0] >= float(alertThresholds.alertEUR_sell):
    message = 'sprzedaj'
    send_to_IFTTT(currency2, get_currency2[0], message)
    print(f'{currency2.upper()}: {get_currency2[0]} // SELL!!!')

# GBP
if get_currency3[0] <= float(alertThresholds.alertGBP_buy):
    message = 'kup'
    send_to_IFTTT(currency3, get_currency3[0], message)
    print(f'{currency3.upper()}: {get_currency3[0]} // BUY!!!')
elif get_currency3[0] >= float(alertThresholds.alertGBP_sell):
    message = 'sprzedaj'
    send_to_IFTTT(currency3, get_currency3[0], message)
    print(f'{currency3.upper()}: {get_currency3[0]} // SELL!!!')
    
# BTC ≥ x.xx USD
if get_currency4[0] >= alertThresholds.alertBTC:
    send_to_IFTTT(currency4, get_currency4[0])
    print(f'{currency4.upper()}: {get_currency4[0]} !!!')

# ------------- BTC yield ------------ #

myBTCprice = 47317 # bought 220103, price from Statista 
BTCyield = get_currency4[0]/myBTCprice
BTCyield = -(100-(get_currency4[0]/myBTCprice)*100)
if BTCyield < 0:
    print(f'NEGATIVE BTC yield at: {BTCyield:.2f}%')
else: 
    print(f'Positive BTC yield at: {BTCyield:.2f}%')

# ---------- calculate trend --------- #

# v1
# TODO: v2

trend = get_currency1[3] + get_currency2[3] + get_currency3[3] # add all trend values from currencies that ran in the function 
print(f'Trend value: {trend}')

if trend > 1: # 2 currencies are trending up
    trend = 'up'
elif trend >= -1: # ups and downs
    trend = 'const'
elif trend < -2: # at least 2 currencies are trending down
    trend = 'down'

print(f'Trend is: {trend}')

# --- open charts from notification -- #

# for macOS
page_url = 'https://www.walutomat.pl/kursy-walut/'

# for Windows
def open_url():
    try: 
        webbrowser.open_new(page_url)
        print('Opening URL...') # status
    except: 
        print('Failed to open URL. Unsupported variable type.')

# ----------- notifications ---------- #

# icons for macOS notifications
iconUp = 'https://i.postimg.cc/FK019QHq/arrow-up.png'
iconConst = 'https://i.postimg.cc/xTkffSsR/minimize.png'
iconDown = 'https://i.postimg.cc/JzVLRHHr/arrow-down.png'

# NOTE: can't write a function notificationMessage()
# win10toast_click\__init__.py", line 140, in _show_toast
    # title))
# TypeError: Objects of type 'function' can not be converted to Unicode.

try:
    if trend == 'up': # if currencies are going up then display relevant icon (arrow up)
        if platform == "darwin": # macOS
            # NOTE: 2/2
            pync.notify(f'{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n{currency4.upper()}: ${get_currency4[0]} {get_currency4[1]} ({BTCyield:.2f}%)', title='Forex update:', contentImage=iconUp, sound="Funk", open=page_url)
        elif platform == "win32": # Windows
            toaster.show_toast(title="Forex update:", msg=f'{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n{currency4.upper()}: ${get_currency4[0]} {get_currency4[1]} ({BTCyield:.2f}%)', icon_path="./icons/v3/arrow-up.ico", duration=None, threaded=True, callback_on_click=open_url) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
    elif trend == 'const': # if currencies are not changing then display relevant icon (+)
        if platform == "darwin": # macOS
            # NOTE: 2/2
            pync.notify(f'{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n{currency4.upper()}: ${get_currency4[0]} {get_currency4[1]} ({BTCyield:.2f}%)', title='Forex update:', contentImage=iconConst, sound="Funk", open=page_url)
        elif platform == "win32": # Windows
            toaster.show_toast(title="Forex update:", msg=f'{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n{currency4.upper()}: ${get_currency4[0]} {get_currency4[1]} ({BTCyield:.2f}%)', icon_path="./icons/v3/minimize.ico", duration=None, threaded=True, callback_on_click=open_url) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
    elif trend == 'down': # if currencies are going down then display relevant icon (arrow down)
        if platform == "darwin": # macOS
            # NOTE: 2/2
            pync.notify(f'{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n{currency4.upper()}: ${get_currency4[0]} {get_currency4[1]} ({BTCyield:.2f}%)', title='Forex update:', contentImage=iconDown, sound="Funk", open=page_url)
        elif platform == "win32": # Windows
            toaster.show_toast(title="Forex update:", msg=f'{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n{currency4.upper()}: ${get_currency4[0]} {get_currency4[1]} ({BTCyield:.2f}%)', icon_path="./icons/v3/arrow-down.ico", duration=None, threaded=True, callback_on_click=open_url) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
except NameError: # variable doesn't exist because file doesn't exist
    # NOTE: First launch or there was a problem with saving the value.
    pass

# ------------- run time ------------- #

end_time = time.time() # run time end 
total_run_time = round(end_time-start_time,2)
print(f"Total script run time: {total_run_time} seconds.")