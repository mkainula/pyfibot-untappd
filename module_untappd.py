import time
import feedparser, json, sqlite3
from twisted.internet import reactor

def init(bot):
        """Called when the bot is loaded and on rehash"""

def command_untappd(bot, user, channel, args):
        args = args.split()
        delay = float(args[0])
        bot.say(channel, "Fetching checkins from untappd with delay %s" % delay)
        fetch_untappd(delay, bot, channel)

def fetch_untappd(delay, bot, channel):

        #IDs of tracked venues
        #TODO: Fetch these from a config file that can be rehashed and configured per channel
        venueIds = "21205", "26889", "31997", "33225", "78709", "32553", "103892", "61907", "45570", "707667", "22335", "117322", "67048", "103902", "84589", "125277", "28363", "595879", "189889", "180323", "29015", "84636", "1625908", "34079", "215220", "93775", "979446", "177055", "127101", "58796", "2051374"

        print("fetching updates...")
        #Init db
        conn = sqlite3.connect("beers.db")
        conn.text_factory = str

        c = conn.cursor()

        for venueId in venueIds:

                #Fetch latest check-ins and parse
                url = "https://untappd.com/rss/venue/" + venueId
                data = feedparser.parse(url)
                for item in data.entries:
                        fullText = item.title
                        # TODO: fixme with regexp magic
                        if(len(fullText.split("drinking a")) < 2):
                                continue
                        splitted = fullText.split("drinking a")[1].split(" at ")
                        splittedBeerName = splitted[0]
                        if(splittedBeerName[0] == 'n'):
                                beerName = splittedBeerName[2:].strip()
                        else:
                                beerName = splittedBeerName.strip()
                        location = splitted[1]

                        print (beerName + ' ' + location)

                        #Check the DB
                        previousAvailability = c.execute('SELECT * FROM beers WHERE beername=? AND venueid=?', (beerName.encode('utf-8'), venueId))
                        if previousAvailability.fetchone() is None:
                                #A new beer was found, store to DB and announce in channel
                                c.execute('INSERT INTO beers VALUES (?, ?, ?, date("now"), ?)', (beerName.encode('utf-8'), location.encode('utf-8'), venueId, item.link))
                                bot.say(channel, "A wild tick appears! %s at %s (%s)" % (beerName, location, item.link))
                        else:
                                #Update last seen
                                c.execute('UPDATE beers SET lastseen=date("now") WHERE beername=? AND venueId=?', (beerName, venueId))

        #Commit to DB
        conn.commit()

        #Loopy loop
        reactor.callLater(delay, fetch_untappd, delay=delay, bot=bot, channel=channel)

