# tar1090-flightlogger
Python Flight logger for recording seen planes to a database

## Why?

Thanks to wiedehopf and his repositories [readsb](https://github.com/wiedehopf/readsb) and [tar1090](https://github.com/wiedehopf/tar1090) I am running an ADS-B flight radar on a Raspberry Pi Zero.

While learning Python I have written a script for recording all seen planes into an SQLite-Database. Sometimes it crashed and only logged the transponder code of the plane. A second script run by a cronjob searched the web for more data like registration, type, airline and manufacturer, and updates the database.

With little knowledge and watching a course for object oriented programming I decided to rewrite my scripts. I integrated the web scraping.

I know this is not perfect. It helped me to learn Python and improve my skills.

## Data logged

I logged basic information in the database:

- icaohex
- registration
- manufacturer
- type
- airline
- firstseen date
- lastseen date
- count

As this is hardcoded it needs some work to change it. I also change or add some data in airplane.py to have consistent data as not all sources use the same format or names for the manufacturer, the type or the airline.

## config.py

In the config.py file some things can and should be configured.

```
    # URL of aircraft.json source file from tar1090 installation
    # see also https://github.com/wiedehopf/tar1090
        self.url="http://your-ip/tar1090/data/aircraft.json"
    # time to wait between URL requests in seconds
        self.sleep=30
    # request tries till timeout
        self.counter=10
    # Location of database file
        self.db="/home/user/dbname"
    # name of database table
        self.table="flights"
    # location of logfile
        self.log="/home/user/logfilename"
    # maximum lines in logfile
        self.loglines=500
    # log in db existing planes / True/False
        self.logexist=False
```

