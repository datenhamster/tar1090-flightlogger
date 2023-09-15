import json
import requests
from urllib.request import urlopen, URLError
from bs4 import BeautifulSoup

class Config():
    def __init__(self):
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

    # define variables for hex-query
        self.registration=""
        self.manufacturer=""
        self.type=""
        self.airline=""
        self.error=""

    # data sources for hex-query
    def try1(self, hex):
        try:
            url="https://api.adsbdb.com/v0/aircraft/" + hex
            self.planedata=json.loads(requests.get(url).content)
            if self.planedata['response']['aircraft']:
                self.registration=self.planedata['response']['aircraft']['registration'].upper()
                self.manufacturer=self.planedata['response']['aircraft']['manufacturer']
                self.type=self.planedata['response']['aircraft']['type']
                self.airline=self.planedata['response']['aircraft']['registered_owner']
            else:
                self.registration="n/a"
        except:
            self.registration="n/a"
            self.error="Fehler: " + url

    def try2(self, hex):
        try:
            url="https://www.live-military-mode-s.eu/military%20mode-s%20database/search/searchMilHex.php?Code=" + hex + "&submit4=Search"
            with urlopen(url) as webpage:
                planedata = BeautifulSoup(webpage.read().decode('latin-1'),features="html.parser")
            td=planedata.find_all("td")
            zlist=[]
            for i in td:
                z=("".join(i.findAll(text=True)))
                zlist.append(z)
            if "Serial:" in zlist:
                self.registration=zlist[zlist.index("Serial:")+1].upper()
                self.manufacturer=""
                self.type=zlist[zlist.index("Type:")+1]
                self.airline=zlist[zlist.index("Operator")+1]
            else:
                self.registration="n/a"
        except:
            self.registration="n/a"
            self.error="Fehler: " + url

    def try3(self, hex):
        try:
            url="https://www.radarbox.com/data/mode-s/" + hex
            with urlopen(url) as webpage:
                planedata = BeautifulSoup(webpage.read().decode('latin-1'),features="html.parser")
            td=planedata.find_all("div")
            zlist=[]
            for i in td:
                z=("".join(i.findAll(text=True)))
                zlist.append(z)
            if "Registration" in zlist:
                self.registration=zlist[zlist.index("Registration")+1].upper().strip()
                self.manufacturer=""
                self.type=zlist[zlist.index("Aircraft Model")+1].strip().replace("'", " ")
                try:
                    self.airline=zlist[zlist.index("Airline/Operator")+1]
                except:
                    self.airline=""
            else:
                self.registration="n/a"
        except:
            self.registration="n/a"
            self.error="Fehler: " + url            

    def try4(self, hex):
        try:
            pass
        except:
            self.registration="n/a"
            #self.error="Fehler: " + url    

    def try5(self, hex):
        try:
            pass
        except:
            self.registration="n/a"
            #self.error="Fehler: " + url    

    def regfind1(self, registration):
        try:
            url="https://www.radarbox.com/data/registration/" + registration
            with urlopen(url) as webpage:
                planedata = BeautifulSoup(webpage.read().decode('latin-1'),features="html.parser")
            td=planedata.find_all("div")
            zlist=[]
            for i in td:
                z=("".join(i.findAll(string=True)))
                zlist.append(z)
            if "Registration" in zlist:
                self.registration=zlist[zlist.index("Registration")+1].upper().strip()
                self.manufacturer=""
                self.type=zlist[zlist.index("Aircraft Model")+1].strip().replace("'", " ")
                try:
                    self.airline=zlist[zlist.index("Airline/Operator")+1]
                except:
                    self.airline=""
            else:
                self.registration="n/a"
        except:
            self.registration="n/a"
            self.error="Fehler: " + url          
