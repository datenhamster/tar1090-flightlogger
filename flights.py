from contextlib import closing
from urllib.request import urlopen, URLError
import urllib.error
import json
import time
from airplane import Airplane
from config import Config
from logger import Logger

counter=1
Logger().startup()
def data_import(url, counter):
    try:
        with closing(urlopen(url, None, 5.0)) as aircraft_file:
            return json.load(aircraft_file)
    except urllib.error.URLError as e:
        Logger().log("Try " + str(counter) + " : " + str(e) + " - " + url)
        if counter < Config().counter:
            return counter
        else:
            Logger().log("Terminated - Timeout")
            quit()
try:
    while True:
        airdata=data_import(Config().url, counter)
        if isinstance(airdata, dict):
            counter=1
            for a in airdata['aircraft']:
                hex=a['hex']
                if hex.startswith("~"):
                    hex=hex[1:]
                if len(hex) > 6:
                    break
                plane=Airplane(hex)
                if plane.checkhex():
                    plane.getdata()
                    if plane.registration.lower().startswith("n/a") or plane.manufacturer=="" or plane.airline=="":
                        Airplane(hex).searchhex('old')
                    else:
                        if Config().logexist:
                            Logger().log("Existing in database: " + plane.hex + " - " + plane.registration + " is a " + plane.manufacturer + " " + plane.type + "\t from " + plane.airline + "\t first contact: " + plane.firstseen + " - " + str(plane.count) + " contacts")
                else:
                    Airplane(hex).searchhex('new')
        else:
            counter=airdata+1
        time.sleep(Config().sleep)
except KeyboardInterrupt:
    Logger().log("KeyboardInterrupt")