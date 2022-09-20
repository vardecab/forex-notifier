# ==================================== #
#            forex-notifier            #
# ==================================== #

# ------------ import libs ----------- #

import time # calculate script's run time
from datetime import datetime # generate timestamp for saving data
import sys # terminate script
import requests # send data via webhook to IFTTT
from inspect import cleandoc # clean up whitespace in multiline strings
import re # regex
import csv # save & read .csv files
import os # create folders

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

# ----- timestamp for saving data ---- #

this_run_datetime = timestamp = datetime.strftime(datetime.now(), '%y%m%d-%H%M%S') # eg 210120-173112

# ----- check and create folders ----- #
# output
if not os.path.isdir("api"):
    os.mkdir("api")
    print(f"Folder created: api")
# comparison_files
if not os.path.isdir("comparison_files"):
    os.mkdir("comparison_files")
    print(f"Folder created: comparison_files")
# csv 
if not os.path.isdir("comparison_files/csv"):
    os.mkdir("comparison_files/csv")
    print(f"Folder created: comparison_files/csv")

# - get main API key and prepare URL - #

API_url = 'https://api.getgeoapi.com/v2/currency/convert' # API URL 
try: 
    API_key = open("./api/CCAP_API-key.txt", "r").read() # read API key from file
except FileNotFoundError: 
    print("Couldn't find Currency API key — script can't work without it. Follow 'How to use' in README / add file to the `api` folder / check file name (`CCAP_API-key.txt`).")
    print("Closing.")
    sys.exit() # terminate script

API_key = f'?api_key={API_key}'
format = '&format=json' # get response from API in JSON

# ------------ crypto URL ------------ #

crypto_API_url = "https://api.binance.com/api/v3/ticker/price" # API URL 

# ---------- functions start --------- #

def getRates(currency, base_currency): 

    currency = currency.upper() # must be in uppercase for API call
    base_currency = base_currency.upper() # must be in uppercase for API call
    
    # --------- get previous rate -------- #
    
    try:   
        with open("./comparison_files/csv/" + currency + ".csv", "r", errors='ignore') as readFile: 
            previous_rate = readFile.readlines()[-1] # read last line of the file
        previous_rate = float((re.search('[0-9]+\.[0-9]+',previous_rate)[0])) # use regex to find rate in the file, remove whitespace, convert string to float
        print(f'Previous {currency} rate loaded.') # status
    except (FileNotFoundError, ValueError, IndexError): # file doesn't exist
        # NOTE: File doesn't exist, 1) first launch or 2) there was a problem with saving the value last time the script ran or 3) file is empty.
        # pass # let's move on 
        previous_rate = '' # let's move on
    
    # --------- get current rate --------- #
    
    try:
        currency_pair = currency + "_" + base_currency # desired currency + base_currency
        currency_pair = f'&from={currency}&to={base_currency}' # build desired currency + base_currency pair
        # print(currency_pair) # debug
        buildURL = API_url + API_key + currency_pair + format
        # print(buildURL) # debug
        get_data = requests.get(url=buildURL).json() # get data from API
        # print(get_data)
        rate = round(float(get_data['rates'][base_currency]['rate']),2) # take value from JSON returned from API and round to 4 decimals
        # print(rate) # debug
    
    # ----- catch if it doesn't work ----- #
    
    except:
        # NOTE: Possible 5## error / API down.
        
        print("Can't access API — check your Internet connection and API Server Status: https://currency.getgeoapi.com/status/")
    
        # URLs for macOS notification 
        error ="https://i.postimg.cc/RZZwrDDH/error.png"
        apiURL = "https://currency.getgeoapi.com/status/"
    
        # open API Server Status from Windows notification
        def open_errorURL():
            try: 
                webbrowser.open_new(apiURL)
                print('Opening URL...') # status
            except: 
                print('Failed to open URL.')
                
        # show notification about the error
        if platform == "darwin": # macOS
            pync.notify(f"Can't access API. Check your Internet connection and API Server Status.", title='forex-notifier', contentImage=error, sound="", open=apiURL)
        elif platform == "win32": # Windows
            toaster.show_toast(title="forex-notifier", msg=f"Can't access API. Check your Internet connection and API Server Status.", icon_path="./icons/v3/error.ico", duration=None, threaded=True, callback_on_click=open_errorURL) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
            
        print("Closing.")
        sys.exit() # close script
        
    # --------------- trend -------------- #

    trend = 0 # based on trend decide which icon to use in notification 

    # show symbols
    try:
        if previous_rate < round(rate,2):
            if platform == 'darwin':
                change_symbol = '⬆️' # emoji
            elif platform == 'win32':
                change_symbol = ">" # Windows neither does display emojis well nor ↑ ↓ in a toast notification 
            trend += 1
        elif previous_rate == round(rate,2): 
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
        # print(f'{currency}: {rate:.2f} {change_symbol} ({previous_rate:.2f})') # :.2f used to always show 2 decimals
        print(f'{currency}: {round(rate,2)} {change_symbol} ({previous_rate:.2f})') # :.2f used to always show 2 decimals
    except (NameError, UnboundLocalError, TypeError): # variable doesn't exist
    #     # NOTE: Variable doesn't exist, either 1) first launch or 2) there was a problem with saving the value last time the script ran.
        # pass # let's move on
        change_symbol = '' # let's move on

    # -- save current rate to file later - #
    
    with open("./comparison_files/csv/" + currency.upper() + ".csv", "a", newline='') as file: # save (append) current rate for comparison in future
        writer = csv.writer(file)
        writer.writerow([timestamp,rate])
        print(f'New {currency.upper()} rate saved in file.') # status

    # ----------- return values ---------- #

    return [rate, change_symbol, previous_rate, trend] # return a list with values to be used in notification
    # NOTE: 1/2: eg. get_currency1[0] => rate; get_currency1[1] => change_symbol; get_currency1[2] => previous_rate, etc.
    
def getCryptoRates(currency):
    # NOTE: MVP 
    
    buildURL_crypto = crypto_API_url + '?symbol=' + currency.upper() # Binance _is_ case-sensitive 
    # print(buildURL_crypto) # debug
    try:
        get_data = requests.get(url=buildURL_crypto).json() # get data from API
        rate = get_data['price'] # get specific value from returned JSON
        rate = round(float(rate),2) # convert str to float 
        # print(get_data) # debug 
    except: # possible server error
        pass # don't worry about crypto, do the rest of the script 
    
    # -- save current rate to file later - #
    
    with open("./comparison_files/csv/" + currency.upper() + ".csv", "a", newline='') as file: # save (append) current rate for comparison in future
        writer = csv.writer(file)
        writer.writerow([timestamp,rate])
        print(f'New {currency.upper()} rate saved in file.') # status
        
    return rate # return value to the variable outside of the function 
    
# ----------- functions end ---------- #

# ----- put your currencies here ----- #

base_currency = 'pln'

currency1 = 'usd' # 1st currency 
currency2 = 'eur' # 2nd currency 
currency3 = 'gbp' # ...
currency4 = 'btcusdt' # 1st crypto; USDT should be 1:1 to USD
currency5 = 'doteur' # 2nd crypto

# ----- run function to get rates ---- #

get_currency1 = getRates(currency1, base_currency)
get_currency2 = getRates(currency2, base_currency)
get_currency3 = getRates(currency3, base_currency)
get_currency4 = getCryptoRates(currency4) # BTC <> EUR
get_currency5 = getCryptoRates(currency5) # DOT <> EUR

# ---- IFTTT automation for alerts --- #

try: 
    ifttt_maker_key = open('./api/IFTTT-key.txt', 'r').read() # read API key
except FileNotFoundError:
    print("Couldn't find IFTTT API key — alerts won't work. Add file to the `api` folder / check file name (`IFTTT-key.txt`) and try again.")
    pass

try: 
    event_name = 'forex' # IFTTT event name which is used in recipes
    webhook_url = f'https://maker.ifttt.com/trigger/{event_name}/with/key/{ifttt_maker_key}' # build URL
except: 
    pass

def send_to_IFTTT(currency, rate, message):
    
    # data passed to IFTTT ↓
    currency = currency.upper() # nice and tidy
    report = {
        "value1": currency,
        "value2": f'{rate:.2f}',
        "value3": message # additional message 
    }
    requests.post(webhook_url, data=report) # send data to IFTTT
    print("Alert sent to IFTTT.") # status

# ----------- custom alerts ---------- #
# TODO: function to avoid unnecessary code -> in progress on 7d0ee2f2

# USD
try:
    if get_currency1[0] <= float(alertThresholds.alertUSD_buy):
        message = 'kup'
        send_to_IFTTT(currency1, get_currency1[0], message)
        print(f'{currency1.upper()}: {get_currency1[0]:.2f} // BUY!!!')
    elif get_currency1[0] >= float(alertThresholds.alertUSD_sell):
        message = 'sprzedaj'
        send_to_IFTTT(currency1, get_currency1[0], message)
        print(f'{currency1.upper()}: {get_currency1[0]:.2f} // SELL!!!')
except: 
    pass

# EUR
try:
    if get_currency2[0] <= float(alertThresholds.alertEUR_buy):
        message = 'kup'
        send_to_IFTTT(currency2, get_currency2[0], message)
        print(f'{currency2.upper()}: {get_currency2[0]:.2f} // BUY!!!')
    elif get_currency2[0] >= float(alertThresholds.alertEUR_sell):
        message = 'sprzedaj'
        send_to_IFTTT(currency2, get_currency2[0], message)
        print(f'{currency2.upper()}: {get_currency2[0]:.2f} // SELL!!!')
except:
    pass

# GBP
try:
    if get_currency3[0] <= float(alertThresholds.alertGBP_buy):
        message = 'kup'
        send_to_IFTTT(currency3, get_currency3[0], message)
        print(f'{currency3.upper()}: {get_currency3[0]:.2f} // BUY!!!')
    elif get_currency3[0] >= float(alertThresholds.alertGBP_sell):
        message = 'sprzedaj'
        send_to_IFTTT(currency3, get_currency3[0], message)
        print(f'{currency3.upper()}: {get_currency3[0]:.2f} // SELL!!!')
except:
    pass
    
# BTC ≥ x.xx USD
# NOTE: won't work after 3.0 update
# if get_currency4[0] >= alertThresholds.alertBTC:
#     message = '' # empty but assigned, otherwise next line will crash without `message` 
#     send_to_IFTTT(currency4, get_currency4[0], message)
#     print(f'{currency4.upper()}: {get_currency4[0]} !!!')

# ------------- BTC yield ------------ #

myBTCprice = 47317 # bought 220103, price from Statista 

# calculate
BTCyield = get_currency4/myBTCprice
BTCyield = -(100-(get_currency4/myBTCprice)*100)

BTCyield = round(BTCyield,2) # round to 2 decimals

if BTCyield < 0:
    print(f'NEGATIVE BTC yield at: {BTCyield}%')
else: 
    BTCyield = '+' + str(BTCyield)
    print(f'Positive BTC yield at: {BTCyield}%')
    
# ------------- DOT yield ------------ #

myDOTpricePL = 30.95 # got 220714, price from Revolut
myDOT = 2.10497474

try: 
    
    # some calculations
    get_currency5 = get_currency5 * get_currency2[0] # get DOT price in PLN by converting to PLN from EUR
    myDOTvalue = myDOT * get_currency5 # calculate how much PLN I have in DOT
    myDOTyield = round(myDOTvalue-(myDOTpricePL*myDOT),2) # calculate yield since I got DOT
    print(myDOTyield)
    if myDOTyield > 0:
        myDOTyield = '+' + str(myDOTyield)
    else: 
        # myDOTyield = '-' + str(myDOTyield) # NOTE: creates double --
        pass
    
    # calculate
    DOTyield = get_currency5/myDOTpricePL
    DOTyield = -(100-(get_currency5/myDOTpricePL)*100) # whoa 
    
    DOTyield = round(DOTyield,2) # round to 2 decimals

    if DOTyield < 0:
        print(f'NEGATIVE DOT yield at: {DOTyield}%')
    else:  
        DOTyield = '+' + str(DOTyield)
        print(f'Positive DOT yield at: {DOTyield}%')
        
except: # possible server error
    pass

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

# NOTE: notification syntax: currency_name: currency_value currency_symbol currency_previous_value
# TODO: simplify notifications to a function, too much repetition

try:
    if trend == 'up': # if currencies are going up then display relevant icon (arrow up)
        if platform == "darwin": # macOS
            # NOTE: 2/2
            pync.notify(
                f"{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n"
                f"{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n"
                f"{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n"
                f"DOT: {myDOTvalue:.2f} zł ({myDOTyield} zł; {DOTyield}%)\n"
                f"{currency4.upper()}: ${get_currency4:.0f} ({BTCyield}%)",
                title='Forex update:', 
                contentImage=iconUp, 
                sound="",
                open=page_url)
        elif platform == "win32": # Windows
            toaster.show_toast(
                title="Forex update:", 
                msg=
                f"{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n"
                f"{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n"
                f"{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n"
                f"DOT: {myDOTvalue:.2f} zł ({myDOTyield} zł; {DOTyield}%)\n"
                f"{currency4.upper()}: ${get_currency4:.0f} ({BTCyield}%)\n",
                icon_path="./icons/v3/arrow-up.ico",
                duration=None,
                threaded=True,
                callback_on_click=open_url) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
    elif trend == 'const': # if currencies are not changing then display relevant icon (+)
        if platform == "darwin": # macOS
            # NOTE: 2/2
            pync.notify(
                f"{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n"
                f"{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n"
                f"{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n"
                f"DOT: {myDOTvalue:.2f} zł ({myDOTyield} zł; {DOTyield}%)\n"
                f"{currency4.upper()}: ${get_currency4:.0f} ({BTCyield}%)",
                title='Forex update:',
                contentImage=iconConst,
                sound="",
                open=page_url)
        elif platform == "win32": # Windows
            toaster.show_toast(
                title="Forex update:", 
                msg=
                f"{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n"
                f"{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n"
                f"{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n"
                f"DOT: {myDOTvalue:.2f} zł ({myDOTyield} zł; {DOTyield}%)\n"
                f"{currency4.upper()}: ${get_currency4:.0f} ({BTCyield}%)\n",
                icon_path="./icons/v3/minimize.ico",
                duration=None,
                threaded=True,
                callback_on_click=open_url) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
    elif trend == 'down': # if currencies are going down then display relevant icon (arrow down)
        if platform == "darwin": # macOS
            # NOTE: 2/2
            pync.notify(
                f"{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n"
                f"{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n"
                f"{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n"
                f"DOT: {myDOTvalue:.2f} zł ({myDOTyield} zł; {DOTyield}%)\n"
                f"{currency4.upper()}: ${get_currency4:.0f} ({BTCyield}%)",
                title='Forex update:',
                contentImage=iconDown,
                sound="",
                open=page_url)
        elif platform == "win32": # Windows
            toaster.show_toast(
                title="Forex update:", 
                msg=
                f"{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n"
                f"{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n"
                f"{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n"
                f"DOT: {myDOTvalue:.2f} zł ({myDOTyield} zł; {DOTyield}%)\n"
                f"{currency4.upper()}: ${get_currency4:.0f} ({BTCyield}%)\n",
                icon_path="./icons/v3/arrow-down.ico",
                duration=None,
                threaded=True,
                callback_on_click=open_url) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
except (NameError, ValueError): # variable doesn't exist because file doesn't exist
    # NOTE: First launch or there was a problem with saving the value, or empty files.
    pass

# ------------- run time ------------- #

end_time = time.time() # run time end 
total_run_time = round(end_time-start_time,2)
print(f"Total script run time: {total_run_time} seconds.")