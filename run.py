# ==================================== #
#            forex-notifier            #
# ==================================== #

# ------------ import libs ----------- #

import time # calculate script's run time
import sys # terminate script
import requests # send data via webhook to IFTTT

# scraper 
from urllib.request import urlopen, Request # open URLs; Request to work around blocked user-agent: https://stackoverflow.com/questions/16627227/
from bs4 import BeautifulSoup # BeautifulSoup; parsing HTML
import ssl # workaround for certificate issue: https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate
import certifi # workaround for certificate issue: https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate

# notifications ↓ 
from sys import platform # check platform (Windows/macOS)
if platform == 'darwin':
    import pync # macOS notifications
elif platform == 'win32':
    from win10toast_click import ToastNotifier # Windows 10/11 notifications
    toaster = ToastNotifier() # initialize win10toast
import webbrowser # open URLs from notification

# import alert thresholds
import alertThresholds # file

# --------- start + run time --------- #

start_time = time.time() # run time start
print("Starting the script...") # status

# ---------------- URL --------------- #

page_url = "https://www.google.com/search?q="

# --------- let the fun begin -------- #

def getRates(currency, base_currency): 
    
    currency = currency.upper() # nice and tidy
    base_currency = base_currency.upper() # nice and tidy

    # --------- get previous rate -------- #
    
    try:
        previous_rate = float(open("./comparison_files/" + currency + ".txt", "r").read()) # read previous rate
        print(f'Previous rate loaded.') # status
    except FileNotFoundError: # file doesn't exist
        #* NOTE: File doesn't exist, 1) first launch or 2) there was a problem with saving the value last time the script ran. 
        pass # let's move on 

    # --------- get current rate --------- #

    try:
        print("Opening page...") # status
        request = Request(page_url + currency + "+" + "to" + "+" + base_currency, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'}) # workaround for: Request -> blocked user agent
        page = urlopen(request, timeout=3, context=ssl.create_default_context(cafile=certifi.where())) # workaround for: context -> certificate issue
    except: # couldn't download data
        print("Wooops. Can't access page to download data. Maybe internet is down? Check if you can access https://www.google.com. Exiting...") # status
        sys.exit()

    print("Scraping page...") # status
    soup = BeautifulSoup(page, 'html.parser') # parse the page
    try: # NOTE: 1st approach — works with "normal" currencies  
        get_rate = soup.select_one("#knowledge-currency__updatable-data-column > div.b1hJbf > div.dDoNo.ikb4Bb.gsrt > span.DFlfde.SwHCTb").attrs.get("data-value", None) # get value from HTML element
        rate = round(float(get_rate),2) 
    except: # NOTE: workaround for BTC     
        get_rate = soup.select_one("#crypto-updatable_2 > div > div:nth-child(2) > span.pclqee").text # get value from HTML element    
        get_rate = get_rate.replace(u'\xa0', u'') # replace weird char
        get_rate = get_rate.replace(u',', u'.') # replace , to . so it can be converted to float
        rate = round(float(get_rate)) # round to 0 decimal places, BTC doesn't need .##
        
    # --------------- trend -------------- #

    trend = 0 # based on trend decide which icon to use in notification 

    # show symbols
    try:
        if previous_rate < rate:
            if platform == 'darwin':
                change_symbol = '⬆️'
            elif platform == 'win32':
                change_symbol = "↑" # Windows doesn't display emojis well in a toast notification
            trend += 1
        elif previous_rate == rate: 
            if platform == 'darwin':
                change_symbol = "↔️"
            elif platform == 'win32':
                change_symbol = '↔' # Windows doesn't display emojis well in a toast notification
        else: 
            if platform == 'darwin':
                change_symbol = '⬇️'
            elif platform == 'win32':
                change_symbol = "↓" # Windows doesn't display emojis well in a toast notification 
            trend -= 1
        print(f'{currency}: {rate:.2f} {change_symbol} ({previous_rate:.2f})') # :.2f used to always show 2 decimals
    except NameError: # variable doesn't exist
    #     #* NOTE: Variable doesn't exist, either 1) first launch or 2) there was a problem with saving the value last time the script ran.
        pass # let's move on

    # ---- save current rate for later --- #

    with open("./comparison_files/" + currency + ".txt", "w") as file: # save current rate for comparison in the next run
        file.write(str((f'{rate:.2f}')))
        print(f'File with {currency} saved.') # status

    # ----------- return values ---------- #

    return [rate, change_symbol, previous_rate, trend] # return a list with values to be used in notification
    #* NOTE: 1/2: eg. get_currency1[0] => rate; get_currency1[1] => change_symbol; get_currency1[2] => previous_rate, etc.
    
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

def send_to_IFTTT(currency, rate):
    
    # data passed to IFTTT ↓
    currency = currency.upper() # nice and tidy
    report = {
        "value1": currency,
        "value2": rate
        # "value3": <value>
    }
    requests.post(webhook_url, data=report) # send data to IFTTT
    print("Alert sent to IFTTT.") # status

# ----------- custom alert ----------- #

# EUR <= x.xx PLN
if get_currency2[0] <= float(alertThresholds.alertEUR):
    send_to_IFTTT(currency2, get_currency2[0])
    print(f'{currency2.upper()}: {get_currency2[0]} !!!')
    
# GBP <= x.xx PLN
# if get_currency3[0] <= alertThresholds.alertGBP:
#     send_to_IFTTT(currency3, get_currency3[0])
#     print(f'{currency3.upper()}: {get_currency3[0]} !!!')

# BTC >= x.xx USD
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

trend = get_currency1[3] + get_currency2[3] + get_currency3[3] # add all trend values from currencies that ran in the function 
print(f'Trend value: {trend}')

if trend > 1: # 2 currencies are trending up
    trend = 'up'
elif trend <= 1 and trend >= -1: # ups and downs
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

#* NOTE: can't write a function notificationMessage()
# win10toast_click\__init__.py", line 140, in _show_toast
    # title))
# TypeError: Objects of type 'function' can not be converted to Unicode.

# TODO: can remove
# # calculate transfer value 
# transferValue = 9236.4 * get_currency3[0]; 

try:
    if trend == 'up':
        if platform == "darwin": # macOS
            #* NOTE: 2/2
            pync.notify(f'{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n{currency4.upper()}: ${get_currency4[0]} {get_currency4[1]} ({BTCyield:.2f}%)', title='Forex update:', contentImage=iconUp, sound="Funk", open=page_url)
        elif platform == "win32": # Windows
            toaster.show_toast(title="Forex update:", msg=f'{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n{currency4.upper()}: ${get_currency4[0]} {get_currency4[1]} ({BTCyield:.2f}%)', icon_path="./icons/v3/arrow-up.ico", duration=None, threaded=True, callback_on_click=open_url) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
    elif trend == 'const':
        if platform == "darwin": # macOS
            #* NOTE: 2/2
            pync.notify(f'{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n{currency4.upper()}: ${get_currency4[0]} {get_currency4[1]} ({BTCyield:.2f}%)', title='Forex update:', contentImage=iconConst, sound="Funk", open=page_url)
        elif platform == "win32": # Windows
            toaster.show_toast(title="Forex update:", msg=f'{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n{currency4.upper()}: ${get_currency4[0]} {get_currency4[1]} ({BTCyield:.2f}%)', icon_path="./icons/v3/minimize.ico", duration=None, threaded=True, callback_on_click=open_url) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
    elif trend == 'down':
        if platform == "darwin": # macOS
            #* NOTE: 2/2
            pync.notify(f'{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n{currency4.upper()}: ${get_currency4[0]} {get_currency4[1]} ({BTCyield:.2f}%)', title='Forex update:', contentImage=iconDown, sound="Funk", open=page_url)
        elif platform == "win32": # Windows
            toaster.show_toast(title="Forex update:", msg=f'{currency1.upper()}: {get_currency1[0]:.2f} {get_currency1[1]} ({get_currency1[2]:.2f})\n{currency2.upper()}: {get_currency2[0]:.2f} {get_currency2[1]} ({get_currency2[2]:.2f})\n{currency3.upper()}: {get_currency3[0]:.2f} {get_currency3[1]} ({get_currency3[2]:.2f})\n{currency4.upper()}: ${get_currency4[0]} {get_currency4[1]} ({BTCyield:.2f}%)', icon_path="./icons/v3/arrow-down.ico", duration=None, threaded=True, callback_on_click=open_url) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
except NameError: # variable doesn't exist because file doesn't exist
    #* NOTE: First launch or there was a problem with saving the value.
    pass

# ------------- run time ------------- #

end_time = time.time() # run time end 
total_run_time = round(end_time-start_time,2)
print(f"Total script run time: {total_run_time} seconds.")