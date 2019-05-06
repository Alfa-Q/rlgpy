# rlgpy
[![Build Status](https://travis-ci.com/Alfa-Q/rlgpy.svg?branch=master)](https://travis-ci.com/Alfa-Q/rlgpy)
[![codecov](https://codecov.io/gh/Alfa-Q/rlgpy/branch/master/graph/badge.svg)](https://codecov.io/gh/Alfa-Q/rlgpy)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/296d889cf67742c590f74334046e12af)](https://www.codacy.com/app/Alfa-Q/rlgpy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Alfa-Q/rlgpy&amp;utm_campaign=Badge_Grade)

Rocket League Garage python package for retrieving trade, item, and achievement data in
JSON format.

<hr>

## Features
-   [x] Scrape trade data with options to use a custom URL containing trade information.
-   [x] Scrape Rocket League item data.
-   [x] Achievement data.

Due to Google captcha built-into the page, adding and auto-bumping trades is not possible. It could
be done using Selenium, but for the purposes of this package I have decided to just leave it as a
data extractor.

<hr>

## Examples of basic usage
```python
  from rlgpy.api import RocketLeagueGarage

  # Each call returns a list of the data in JSON format.
  item_data  = RocketLeagueGarage.get_items()
  trade_data = RocketLeagueGarage.get_trades()
  achievement_data = RocketLeagueGarage.get_achievements()

  # Trade data can be extracted from any page containing trades!
  # Example using page with filter parameters in the URL:
  url = 'https://rocket-league.com/trading?filterItem=1709&filterCertification=0&filterPaint=0&filterPlatform=0&filterSearchType=1'
  trade_data = RocketLeagueGarage.get_trades(url=url)

  # Example using page of someone's profile:
  url = 'https://rocket-league.com/trades/KizunaAi'
  trade_data = RocketLeagueGarage.get_trades(url=url)
```
