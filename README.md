# forex-notifier

![Actively Maintained](https://img.shields.io/badge/Maintenance%20Level-Actively%20Maintained-green.svg)

![](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-blue)

>Simple script to show forex rates as Windows 10/11 / macOS notification.

## Screenshots

### Windows

![0](https://user-images.githubusercontent.com/6877391/143601416-f47e87d5-6a51-4657-905c-819a2b9cc368.jpg)

### macOS
![1@2x](https://user-images.githubusercontent.com/6877391/143601426-0c3242fd-d0ad-4af3-ab60-926217f34f0b.jpg)
![2](https://i.postimg.cc/FzDcCr58/screenshot.png)

## How to use

### API key 

- Get API key (for free, takes 2 mins) from [here](https://currency.getgeoapi.com).
- Create `api` folder in the root of the project.
- Create `CCAP_API-key.txt` file in `api` folder.
- Add your API key to that file and save it.

### `run.py`

- Values are in PLN. In order to change that, change `base_currency` variable.
- Change `currency1` … `currency{#}` to desired currencies.

In both, use codes from [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217).

- <s><i>(🚧 temporary) If you don't want to use IFTTT (it's free) then you need to remove all references to IFTTT in the code.</i></s> IFTTT is now optional as of v2.1.

### `alertThresholds.py` 

- Modify this file with desired values to get alerts via IFTTT.

## Release History

- 3.8: Disabled crypto; disabled alerts; reverted emojis to symbols on Windows because Windows doesn't support [country flag emojis](https://emojipedia.org/flags/#:~:text=except%20Windows%2C%C2%A0which%C2%A0displays%20two%2Dletter%20country%20codes%20instead%20of%20emoji%20flag%20images).
- 3.7: Minor text change.
- 3.6: Changed currency 3-letter codes to emoji flags in notifications.
- 3.5: Added IFTTT alert for DOT.
- 3.4.1: Fixed double `--` in notification when DOT yield is negative.
- 3.4: Experimenting with auto updating repo.
- 3.3.1: Added +/- signs to DOT yield notifications.
- 3.3: Added DOT yield to notifications.
- 3.2: Changed rate recording to `.csv` from `.txt`; added some checks to create folders if they're not present; improved texts in console.
- 3.1: Added continuous rate recording — appending values to the files rather than replacing them on each run.
- 3.0.0: Changed API to [Currency API by API PLANT](https://currency.getgeoapi.com) because the old API wasn't showing correct values (probably outdated/cached ones from several days prior); added more catchers for exceptions to prevent script from failing.

<details>

<summary>
Click to see all updates < 3.0.0
</summary>

- 2.1.3: Further cleaning of notifications — this time to the code.
- 2.1.2: Further notifications' text cleaning.
- 2.1.1: Fixed regression bug and cleaned the text in notifications.
- 2.1: Added [Binance API](https://binance-docs.github.io/apidocs/spot/en/) to get rates of different coins. 
- 2.0.3: Added notification when API is down.
- 2.0.2: Made IFTTT alerts optional.
- 2.0.1: Switched to showing 4 decimals in alerts (left 2 decimals for everything else); added `try` & `except` for alerts so the script doesn't break if some thresholds are empty / disabled.
- 2.0.0: Google scraper is failing to obtain values so re-using previous API used in 0.x versions; added buy/sell notifications via IFTTT.
</details>

<details>

<summary>
Click to see all updates < 2.0.0
</summary>

- 1.1: Added BTC; tweaked some text and comments.
- 1.0.2: Moved alert thresholds to a separate file.
- 1.0.1: Tiny tweak in Windows notifications' title.
- 1.0.0: Instead of using API the script is scraping Google; switched back to showing 2 instead of 3 decimals; fixed Windows notifications' text; added some more comments.
</details>

<details>

<summary>
Click to see all updates < 1.0.0
</summary>

- 0.11: Windows notifications: tested & improved + added icons; added API status to README.
- 0.10.1: Changed URLs for icons used in macOS notifications; switched from showing 2 to 3 decimals; small tweak to how trend is calculated.
- 0.10: Added custom alerts via IFTTT (using webhook).
- 0.9: Click notification to go to URL with charts.
- 0.8: Notification icon is selected based on the trend.
- 0.7: Cleaned the structure a bit; switched to use variables `base_currency` & `currency#` to get rates.
- 0.6: Notifications re-enabled.
- 0.5: Added a branch with function to reduce SLOC (-35%). Notifications disabled.
- 0.4.1: Tiny bug fix related to variable.
- 0.4: Added comparison with previous values from the last script run.
- 0.3: v1 of notifications added.
- 0.2: Improved code so only the currency pair rate is shown without JSON stuff.
- 0.1: Initial release.
</details>

<br>

## Versioning

Using [SemVer](http://semver.org/).

## License

![](https://img.shields.io/github/license/vardecab/forex-notifier)

## Acknowledgements

- [Currency API by API PLANT](https://currency.getgeoapi.com) 
- [Binance API](https://binance-docs.github.io/apidocs/spot/en/)
- Icons from [Flaticon](https://www.flaticon.com)
- [IFTTT](https://ifttt.com)
### Notifications
- Windows: [win10toast-click](https://github.com/vardecab/win10toast-click)
- macOS: [pync](https://github.com/SeTeM/pync)

## Contributing

![](https://img.shields.io/github/issues/vardecab/forex-notifier)

If you found a bug or want to propose a feature, feel free to visit [the Issues page](https://github.com/vardecab/forex-notifier/issues).
