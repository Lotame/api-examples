# The Lotame API

Interactive documentation for the Lotame API is available at https://api.lotame.com/docs. The interactive nature of these docs is "live", which means that any write operations you perform are carried out against your real account as if you had done the same operation via the UI. As such, be careful.

# Dependencies

* The python examples use http://www.python-requests.org/en/latest/

# Warnings

* Generally speaking, the examples are just that, examples. They are not highly robust and secure applications. As just one example of this, some will accept the API username and password as command line arguments, but make no attempt to hide those from operating system process listings, etc...
* Depending on the configuration and completeness of your local environment you may see "InsecurePlatformWarning"'s when running these scripts, as all HTTP requests use SSL and require a fully functioning SSL environment via urllib3

# License

Copyright (c) 2015 Lotame Solutions, Inc.

Published under The MIT License, see LICENSE