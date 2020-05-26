# The Lotame API

Interactive documentation for the Lotame API is available at https://api.lotame.com/docs. The interactive nature of these docs is "live", which means that any write operations you perform are carried out against your real account as if you had done the same operation via the UI. As such, be careful.

# better_lotameapi

All of the scripts found in this repo rely on the [better_lotameapi.py module](https://github.com/Lotame/api-examples/blob/master/py/better_lotameapi.py), which was written to be a more elegant way to work with the Lotame API. You are welcome to use it with your own scripts.

Please be sure to configure a [lotame.ini file](https://github.com/Lotame/api-examples/blob/master/py/lotame.ini) to sit alongside better_lotameapi.py.

# Dependencies

These Python 3.6+ examples rely on [Requests](https://requests.readthedocs.io/en/master/). In most cases, the easiest way to install that is via pip:

```pip install requests```

Some examples also rely on [openpyxl](https://openpyxl.readthedocs.io/en/stable/) for working with .xlsx files.

```pip install openpyxl```

# A Note

Please note that the examples contained in this repo are just that: Examples. They're meant to help you get acquainted and comfortable with the Lotame API, but they are not necessarily right for you or your environment. The Support team at Lotame doesn't provide support for these scripts.

# License

Copyright (c) 2020 Lotame Solutions, Inc.

Published under The MIT License, see LICENSE
