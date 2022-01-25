# forex-notifier

![](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-blue)

>Simple script to show forex rates as Windows 10/11 / macOS notification.

## Screenshots

Windows:
![0](https://user-images.githubusercontent.com/6877391/143601416-f47e87d5-6a51-4657-905c-819a2b9cc368.jpg)
macOS:
![1@2x](https://user-images.githubusercontent.com/6877391/143601426-0c3242fd-d0ad-4af3-ab60-926217f34f0b.jpg)
![2](https://i.postimg.cc/FzDcCr58/screenshot.png)


<!-- ## How to use

Lorem ipsum -->

<!-- ## Roadmap

- Lorem ipsum
- Lorem ipsum
- Lorem ipsum -->

## Release History

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

- Icons from [Flaticon](https://www.flaticon.com)

## Contributing

![](https://img.shields.io/github/issues/vardecab/forex-notifier)

If you found a bug or want to propose a feature, feel free to visit [the Issues page](https://github.com/vardecab/forex-notifier/issues).