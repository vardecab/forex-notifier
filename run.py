# ==================================== #
#            forex-notifier            #
# ==================================== #

# ------------ import libs ----------- #

import requests # access API URL 
import time # calculate script's run time
import sys # terminate script
# notifications ↓ 
from sys import platform # check platform (Windows/macOS)
if platform == 'win32':
    from win10toast_click import ToastNotifier # Windows 10/11 notifications
    toaster = ToastNotifier() # initialize win10toast
elif platform == 'darwin':
    import pync # macOS notifications
import webbrowser # open URLs from notification

# --------- start + run time --------- #

start_time = time.time() # run time start
print("Starting the script...")

# ------------- build URL ------------ #

API_url = 'https://free.currconv.com/api/v7/convert' # API URL 
try: 
    API_key = open("./api/TFCC_API-key.txt", "r").read() # read API key from file
except FileNotFoundError: 
    print("Couldn't find The Free Currency Converter API key. Add file to the folder / check file name.")
    print("Closing...")
    sys.exit() # terminate script
    
API_key = '?apiKey='+API_key # join URL parameter with value
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
        #* NOTE: File doesn't exist, 1) first launch or 2) there was a problem with saving the value last time the script ran. 
        pass # let's move on 

    # --------- get current rate --------- #
    
    currency_pair = currency + "_" + base_currency # desired currency + base_currency
    get_data = requests.get(url=API_url + API_key + '&q=' + currency_pair + compact).json() # get data from API
    rate = round(get_data[currency_pair]['val'],2) # currency pair rate rounded to 2 decimals
    
    # --------------- trend -------------- #
    
    trend = 0 # based on trend decide which icon to use in notification 
    
    # ----------- show symbols ----------- #
    try:
        if previous_rate < rate:
            change_symbol = '⬆️'
            trend += 1
        elif previous_rate == rate: 
            change_symbol = '↔️'
        else: 
            change_symbol = '⬇️'
            trend -= 1
        print(f'{currency}: {rate} {change_symbol} ({previous_rate})')
    except NameError: # variable doesn't exist
        #* NOTE: Variable doesn't exist, either 1) first launch or 2) there was a problem with saving the value last time the script ran.
        pass # let's move on
    
    # ---- save current rate for later --- #
    
    with open("./comparison_files/" + currency + ".txt", "w") as file: # save current rate for comparison in the next run
        file.write(str(rate))
        # print(f'File {file} saved.') # status
    
    # ----------- return values ---------- #
    
    return [rate, change_symbol, previous_rate, trend] # return a list with values to be used in notification 
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

# ---- IFTTT automation for alerts --- #

try: 
    ifttt_maker_key = open('./api/IFTTT-key.txt', 'r').read() # read API key
except FileNotFoundError:
    print("Couldn't find IFTTT API key. Add file to the folder / check file name.")
    print("Closing...")
    sys.exit() # terminate script

event_name = 'forex' 
webhook_url = f'https://maker.ifttt.com/trigger/{event_name}/with/key/{ifttt_maker_key}'

def send_to_IFTTT(currency, rate):
    # data passed to IFTTT
    currency = currency.upper() # nice and tidy
    report = {
        "value1": currency,
        "value2": rate
        # "value3": <value>
    }
    requests.post(webhook_url, data=report) # send data to IFTTT
    print("Alert sent to IFTTT.")

# ----------- custom alert ----------- #

# EUR <= 4.60 PLN
if get_currency2[0] <= 4.60:
    send_to_IFTTT(currency2, get_currency2[0])
    print(f'{currency2.upper()}: {get_currency2[0]} !!!')
    
# GBP <= 5.50 PLN
if get_currency3[0] <= 5.50:
    send_to_IFTTT(currency3, get_currency3[0])
    print(f'{currency3.upper()}: {get_currency3[0]} !!!')

# ---------- calculate trend --------- #

# v1

trend = get_currency1[3] + get_currency2[3] + get_currency3[3] # add all trend values from currencies that ran in the function 
print(f'Trend value: {trend}')

if trend >= 2: # 2 currencies are trending up
    trend = 'up'
elif trend <= 1 and trend >= -1: # ups and downs
    trend = 'const'
elif trend <= -2: # at least 2 currencies are trending down
    trend = 'down'
    
print(f'Trend is: {trend}')

# --- open charts from notification -- #

# for macOS
page_url = 'https://www.walutomat.pl/kursy-walut/'

# for Windows
def open_url():
    try: 
        webbrowser.open_new(page_url)
        print('Opening URL...')  
    except: 
        print('Failed to open URL. Unsupported variable type.')

# ----------- notifications ---------- #

try:
    if trend == 'up':
        if platform == "darwin": # macOS
            #* NOTE: 2/2
            pync.notify(f'{currency1.upper()}: {get_currency1[0]} {get_currency1[1]} ({get_currency1[2]})\n{currency2.upper()}: {get_currency2[0]} {get_currency2[1]} ({get_currency2[2]})\n{currency3.upper()}: {get_currency3[0]} {get_currency3[1]} ({get_currency3[2]})', title='Forex update:', contentImage="https://cdn-icons.flaticon.com/png/512/3148/premium/3148312.png?token=exp=1637320365~hmac=e35848f7c1414dcf0998a9700363dd8c", sound="Funk", open=page_url)
        elif platform == "win32": # Windows
            # TODO: check if it works 
            toaster.show_toast(title="Forex update", msg=f'{currency1.upper()}: {get_currency1[0]} {get_currency1[1]} ({get_currency1[2]})\n{currency2.upper()}: {get_currency2[0]} {get_currency2[1]} ({get_currency2[2]})\n{currency3.upper()}: {get_currency2[0]} {get_currency2[1]} ({get_currency2[2]})', icon_path="", duration=None, threaded=True, callback_on_click=open_url) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
    elif trend == 'const':
        if platform == "darwin": # macOS
            #* NOTE: 2/2
            pync.notify(f'{currency1.upper()}: {get_currency1[0]} {get_currency1[1]} ({get_currency1[2]})\n{currency2.upper()}: {get_currency2[0]} {get_currency2[1]} ({get_currency2[2]})\n{currency3.upper()}: {get_currency3[0]} {get_currency3[1]} ({get_currency3[2]})', title='Forex update:', contentImage="https://cdn-icons.flaticon.com/png/512/3148/premium/3148400.png?token=exp=1637320306~hmac=0b5e2a5f5a2edaf0f24700f8bff71a7b", sound="Funk", open=page_url)
        elif platform == "win32": # Windows
            # TODO: check if it works 
            toaster.show_toast(title="Forex update", msg=f'{currency1.upper()}: {get_currency1[0]} {get_currency1[1]} ({get_currency1[2]})\n{currency2.upper()}: {get_currency2[0]} {get_currency2[1]} ({get_currency2[2]})\n{currency3.upper()}: {get_currency2[0]} {get_currency2[1]} ({get_currency2[2]})', icon_path="", duration=None, threaded=True, callback_on_click=open_url) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
    elif trend == 'down':
        if platform == "darwin": # macOS
            #* NOTE: 2/2
            pync.notify(f'{currency1.upper()}: {get_currency1[0]} {get_currency1[1]} ({get_currency1[2]})\n{currency2.upper()}: {get_currency2[0]} {get_currency2[1]} ({get_currency2[2]})\n{currency3.upper()}: {get_currency3[0]} {get_currency3[1]} ({get_currency3[2]})', title='Forex update:', contentImage="https://cdn-icons.flaticon.com/png/512/3148/premium/3148295.png?token=exp=1637320361~hmac=895a71f03d776c45d98e619226eff099", sound="Funk", open=page_url)
        elif platform == "win32": # Windows
            # TODO: check if it works 
            toaster.show_toast(title="Forex update", msg=f'{currency1.upper()}: {get_currency1[0]} {get_currency1[1]} ({get_currency1[2]})\n{currency2.upper()}: {get_currency2[0]} {get_currency2[1]} ({get_currency2[2]})\n{currency3.upper()}: {get_currency2[0]} {get_currency2[1]} ({get_currency2[2]})', icon_path="", duration=None, threaded=True, callback_on_click=open_url) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
except NameError: # variable doesn't exist because file doesn't exist
    #* NOTE: First launch or there was a problem with saving the value.
    pass

# ------------- run time ------------- #

end_time = time.time() # run time end 
total_run_time = round(end_time-start_time,2)
print(f"Total script run time: {total_run_time} seconds.")