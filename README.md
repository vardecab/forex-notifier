# forex-notifier

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

- Get API key (for free, takes 2 mins) from [here](https://free.currencyconverterapi.com).
- Create `api` folder in the root of the project.
- Create `TFCC_API-key.txt` file in `api` folder.
- Add your API key to that file and save it.

### `run.py`

- Values are in PLN. In order to change that, change `base_currency` variable.
- Change `currency1` … `currency4` to desired currencies.

In both, use codes from [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217).

- (🚧 temporary) If you don't want to use IFTTT (it's free) then you need to remove all references to IFTTT in the code.

### `alertThresholds.py` 

- Modify file with desired values.

## Release History

- 2.0.2: Made IFTTT alerts optional.
- 2.0.1: Switched to showing 4 decimals in alerts (left 2 decimals for everything else); added `try` & `except` for alerts so the script doesn't break if some thresholds are empty / disabled.
- 2.0.0: Google scraper is failing to obtain values so re-using previous API used in 0.x versions; added buy/sell notifications via IFTTT.
- 1.1: Added BTC; tweaked some text and comments.
- 1.0.2: Moved alert thresholds to a separate file.
- 1.0.1: Tiny tweak in Windows notifications' title.
- 1.0.0: Instead of using API the script is scraping Google; switched back to showing 2 instead of 3 decimals; fixed Windows notifications' text; added some more comments.

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

- [Free Currency Converter API](https://free.currencyconverterapi.com)
- Icons from [Flaticon](https://www.flaticon.com)
- [IFTTT](https://ifttt.com)
### Notifications
- Windows: [win10toast-click](https://github.com/vardecab/win10toast-click)
- macOS: [pync](https://github.com/SeTeM/pync)

## Contributing

![](https://img.shields.io/github/issues/vardecab/forex-notifier)

If you found a bug or want to propose a feature, feel free to visit [the Issues page](https://github.com/vardecab/forex-notifier/issues).