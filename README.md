pyfibot-untappd
===============

Untappd module for Pyfibot IRC bot (https://github.com/lepinkainen/pyfibot) intended for hard core beer tickers. Periodically checks the RSS feeds of the venues, adds beers to a local SQLite database and sends a message to the IRC channel if a new beer was found for that venue. 

## Tech stack ##

* Python
* SQLite
* Feedparser
* Twisted

## Running ##

Add module_untappd.py to your pyfibot configuration and type
    .untappd <delay>
on the IRC channel you want to run the bot on. For the default venues (craft beer bars in Helsinki and Espoo), you should use at least 10 minutes (600.0) as the delay.

## TODO ##

The current version is quite hacky and intended for single channel&location use only. For usage with multiple cities, at least the following changes would be needed
* Dynamic configuration which would allow reloading/rehashing venues on the fly
* Venues per channel
* Add a command to search when a beer was last seen (should be straightforward as the data is already stored to DB)



