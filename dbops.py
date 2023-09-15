import sqlite3
from config import Config

class DBOps:
    def __init__(self):
        self.con=sqlite3.connect(Config().db)
        self.table=Config().table
        self.statement=""
    def checkdb(self):
        istable=self.con.execute("SELECT name FROM sqlite_master WHERE name='" + self.table + "'").fetchall()
        if istable == []:
            DBOps().createdb()
    def createdb(self):
        statement="CREATE TABLE " + self.table + " ( id integer PRIMARY KEY, icaohex tinytext, registration tinytext, manufacturer text, type text, airline text, firstseen date, lastseen date, count integer )"
        self.con.execute(statement)
    def dbquery(self, statement):
        return self.con.execute(statement).fetchall()
    def dbwrite(self, statement):
        self.con.execute(statement)
        self.con.commit()
    def __del__(self):
        self.con.close()