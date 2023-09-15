import sqlite3
import time
from dbops import DBOps
from logger import Logger
from config import Config

class Airplane:
    def __init__(self, hex):
        DBOps().checkdb()
        self.hex=hex
        self.registration=""
        self.manufacturer=""
        self.type=""
        self.airline=""
        self.firstseen=""
        self.lastseen=""
        self.count=""
        self.zeit=str(time.strftime("%d.%m.%Y"))
        self.dbqhex="SELECT * FROM " + DBOps().table + " WHERE icaohex='" + self.hex + "'"
        self.updatecount="UPDATE " + DBOps().table + " SET lastseen='" + self.zeit + "', count=count+1 WHERE icaohex='" + hex + "'"
    def getdata(self):
        planedata=DBOps().dbquery(self.dbqhex)
        for i in planedata:
            self.registration=i[2]
            self.manufacturer=i[3]
            self.type=i[4]
            self.airline=i[5]
            self.firstseen=i[6]
            self.lastseen=i[7]
            self.count=i[8]
        if self.lastseen != self.zeit:
            DBOps().dbwrite(self.updatecount)
    def checkhex(self):
        planedata=DBOps().dbquery(self.dbqhex)
        return planedata

    def searchhex(self, status):
            planedata=Config()
            planedata.try1(self.hex)
            if planedata.registration=="n/a":
                planedata.try2(self.hex)
                if planedata.registration=="n/a":
                    planedata.try3(self.hex)
                    if planedata.registration=="n/a":
                        planedata.try4(self.hex)
                        if planedata.registration=="n/a":
                            planedata.try5(self.hex)
            if planedata.type.startswith("-") or planedata.airline.startswith("-") or planedata.manufacturer=="":
                if not planedata.registration.lower().startswith("n/a"):
                    planedata.regfind1(planedata.registration)
            if planedata.registration.startswith("-") or planedata.registration.startswith("<!DOCTYPE"):
                planedata.registration="n/a"
            planedata.manufacturer, planedata.type = self.cleanman(planedata.manufacturer, planedata.type)
            planedata.airline = self.cleanairline(planedata.airline, planedata.type)
            if status == 'old':
                statement="UPDATE " + DBOps().table + " SET registration='" + planedata.registration + "', manufacturer='" + planedata.manufacturer + "', type='" + planedata.type + "', airline='" + planedata.airline + "' WHERE icaohex='" + self.hex + "'"
                Logger().log("Update plane: " + self.hex + " - " + planedata.registration + " is a " + planedata.manufacturer + " - " + planedata.type + "\t from " + planedata.airline)
                DBOps().dbwrite(statement)
            else:
                statement="INSERT INTO " + DBOps().table + " (icaohex, registration, manufacturer, type, airline, firstseen, lastseen, count) VALUES ('" + str(self.hex) + "','" + planedata.registration + "','" + planedata.manufacturer + "','" + planedata.type + "','" + planedata.airline + "','" + self.zeit + "','" + self.zeit + "','1')"
                Logger().log("New plane: " + self.hex + " - " + planedata.registration + " is a " + planedata.manufacturer + " - " + planedata.type + "\t from " + planedata.airline)
                try:
                    DBOps().dbwrite(statement)
                except sqlite3.OperationalError as e:
                    Logger().log(e)
            if planedata.error != "":
                Logger().log(planedata.error)

    def cleanman(self, manufacturer ,type):
        search=[
            ["a-22", "Aeroprakt", ""],
            ["aeroprakt ", "Aeroprakt", "cut"],
            ["aerospatiale ", "Avions de Transport Regional", "cut"],
            ["wt9", "Aerospool", ""],
            ["aerospool ", "Aerospool", "cut"],
            ["sea", "AgustaWestland", ""],
            ["lynx", "AgustaWestland", ""],
            ["airbus ", "Airbus", "cut"],
            ["a22", "Airbus", ""],
            ["a3", "Airbus", ""],
            ["kc-30", "Airbus", ""],
            ["various a", "Airbus", "Testflight Various Airframes"],
            ["ec-645", "Airbus Helicopters", "H145M"],
            ["ec645", "Airbus Helicopters", ""],
            ["ec-135", "Airbus Helicopters", ""],
            ["mbb", "Airbus Helicopters", ""],
            ["tiger", "Airbus Helicopters", ""],
            ["coug", "Airbus Helicopters", "H215M"],
            ["h145", "Airbus Helicopters", ""],
            ["eurocopter ", "Airbus Helicopters", "cut"],
            ["a40", "Airbus Military", ""],
            ["pioneer", "Alpi Aviation", ""],
            ["american ", "American-General", "cut"],
            ["antonov ", "Antonov", "cut"],
            ["an-", "Antonov", ""],
            ["aquila ", "Aquila", "cut"],
            ["aquila\t", "Aquila", "cut"],
            ["atr ", "Avions de Transport Regional", ""],
            ["avions de transport regional ", "Avions de Transport Regional", "cut"],
            ["beech ", "Beech", "cut"],
            ["beech+é-á", "Beech", "cut"],
            ["king", "Beech", ""],
            ["be20", "Beech", "B200 King Air"],
            ["bon", "Beech", ""],
            ["g3", "Beech", ""],
            ["musket", "Beech", ""],
            ["raytheon ", "Beech", "cut"],
            ["407", "Bell", ""],
            ["blackwing ", "Blackwing", "cut"],
            ["boeing ", "Boeing", "cut"],
            ["7_7", "Boeing", ""],
            ["B378", "Boeing", ""],
            ["p-8", "Boeing", ""],
            ["c-40", "Boeing", ""],
            ["challenger", "Bombardier", ""],
            ["glob", "Bombardier", ""],
            ["learjet 45", "Bombardier", ""],
            ["dhc-8", "Bombardier", ""],
            ["crj", "Bombardier", ""],
            ["bombardier ", "Bombardier", "cut"],
            ["canadair ", "Bombardier", "cut"],
            ["bae ", "British Aerospace", "cut"],
            ["atlan", "Breguet", ""],
            ["bris", "BRM", ""],
            ["brm aero ", "BRM", "cut"],
            ["bs", "Blackshape", ""],
            ["c42", "Comco Ikarus", ""],
            ["ikarus ", "Comco Ikarus", "cut"],
            ["cessna ", "Cessna", "cut"],
            ["cessna\t", "Cessna", "cut"],
            ["cit", "Cessna", ""],
            ["560", "Cessna", ""],
            ["columbia Aircraft Mfg ", "Cessna", "cut"],
            ["columbia ", "Cessna", "cut"],
            ["1_2", "Cessna", ""],
            ["cirrus ", "Cirrus Design", "cut"],
            ["sr2", "Cirrus Design", ""],
            ["commander 114", "Commander Aircraft", ""],
            ["tbm 940", "DAHER", ""],
            ["dassault ", "Dassault", "cut"],
            ["falc", "Dassault", ""],
            ["diamond Aircraft", "Diamond Aircraft", "Diamond Star"],
            ["diamond", "Diamond Aircraft", ""],
            ["da62", "Diamond Aircraft", ""],
            ["da50", "Diamond Aircraft", ""],
            ["twin star", "Diamond Aircraft", ""],
            ["dornier ", "Dornier", "cut"],
            ["ta-4", "Douglas", ""],
            ["mcr-", "Dyn Aero", ""],
            ["c295", "EADS CASA", ""],
            ["ea5", "Eclipse Aviation", ""],
            ["lega", "Embraer", ""],
            ["pheno", "Embraer", ""],
            ["embraer ", "Embraer", "cut"],
            ["emb", "Embraer", ""],
            ["line", "Embraer", ""],
            ["erj", "Embraer", ""],
            ["praetor", "Embraer", ""],
            ["ea.3", "Extra", ""],
            ["ef", "Eurofighter", ""],
            ["typh", "Eurofighter", ""],
            ["fokker ", "Fokker", "cut"],
            ["f-16", "General Dynamics", ""],
            ["general dynamic ", "General Dynamics", "cut"],
            ["g-2000", "Grobholz", ""],
            ["e-550", "Gulfstream Aerospace", ""],
            ["c-37", "Gulfstream Aerospace", ""],
            ["g2", "Gulfstream Aerospace", ""],
            ["g55", "Gulfstream Aerospace", ""],
            ["g65", "Gulfstream Aerospace", ""],
            ["gvii", "Gulfstream Aerospace", ""],
            ["giv", "Gulfstream Aerospace", ""],
            ["gulfstream Aerospace ", "Gulfstream Aerospace", "cut"],
            ["uc-12w", "Hawker Beechcraft Corp", ""],
            ["hawker", "Hawker Beechcraft Corp", ""],
            ["125 8", "Hawker Beechcraft Corp", ""],
            ["honda", "Honda Aircraft Company", ""],
            ["lancair e", "Lancair International", ""],
            ["lockheed ", "Lockheed", "cut"],
            ["p-3", "Lockheed", ""],
            ["kc-130", "Lockheed", ""],
            ["c-130", "Lockheed", ""],
            ["mc-130", "Lockheed", ""],
            ["maule ", "Maule", "cut"],
            ["mcDonnell_Douglas ", "McDonnell Douglas", "cut"],
            ["dc-9", "McDonnell Douglas", ""],
            ["mooney ", "Mooney", "cut"],
            ["m.20", "Mooney", ""],
            ["nh90", "NH Industries", ""],
            ["nh-90", "NH Industries", ""],
            ["t-28", "North American", ""],
            ["rq-4", "Northrop Grumman", ""],
            ["torn", "Panavia", ""],
            ["piaggio ", "Piaggio", "cut"],
            ["p-180", "Piaggio", ""],
            ["pilatus ", "Pilatus", "cut"],
            ["pc-", "Pilatus", ""],
            ["piper ", "Piper", "cut"],
            ["piper\t", "Piper", "cut"],
            ["pa-", "Piper", ""],
            ["c-145", "PZL", ""],
            ["400 xp", "Raytheon Aircraft Company", ""],
            ["dr.400", "Robin", ""],
            ["robinson ", "Robinson Helicopter", "cut"],
            ["r44", "Robinson Helicopter", ""],
            ["Saab ", "Saab", "cut"],
            ["340", "Saab", ""],
            ["ch-53", "Sikorsky", ""],
            ["socata ", "Socata", "cut"],
            ["metro", "Swearingen", ""],
            ["tecnam ", "Tecnam", "cut"],
            ["p.20", "Tecnam", ""],
            ["c-160", "Transall", ""],
            ["various", "Unknown", ""],
        ]
        for j in search:
            if type.lower().startswith(j[0]):
                manufacturer=j[1]
                if j[2]=="cut":
                    type=type[len(j[0]):]
                elif j[2]=="":
                    type=type
                else:
                    type=j[2]        
        searchman=[
            ["euroc", "Airbus Helicopters", ""],
            ["text", "Cessna", ""],
        ]
        for j in searchman:
            if manufacturer.lower().startswith(j[0]):
                manufacturer=j[1]
        changeman=[
            ["bombardier", "a220", "Airbus"],
            ["lancair", "350", "Cessna"],
            ["columbia", "400", "Cessna"],
        ]
        for j in changeman:
            if manufacturer.lower().startswith(j[0]) and type.lower().startswith(j[1]):
                manufacturer=j[2]
        searchtype=[
            ["aircraft co\t", "Cessna", "cut"],
            ["aquila ", "Aquila", "cut"],
            ["ag5b", "AG-5B Tiger", ""],
            ["c series ", "A220 ", "rp"],
            ["lynx", "Sea ", "add"],
            ["nh-90", "NH90-", "rp"],
            ["nh90 ", "NH90-", "rp"],
            ["nh90n", "NH90-N", "rp"],
        ]        
        for j in searchtype:
            if type.lower().startswith(j[0]):
                if j[2]=="cut":
                    type=type[len(j[0]):]
                if j[2]=='add':
                    type=j[1]+type
                if j[2]=='rp':
                    type=j[1]+type[len(j[0]):]
                else:
                    type=j[1]
        return manufacturer, type

    def cleanairline(self, airline, type):
        search=[
            ["","Airbus","Testflight Various Airframes"],
            ["baf", "Belgian Air Component", ""],
            ["private owner", "Private", ""],
            ["civil", "Private", ""],
        ]        
        for j in search:
            if airline.lower().startswith(j[0]):
                if j[2]=="":
                    airline=j[1]
                else:
                    if type==j[2]:
                        airline=j[1]
        return airline
