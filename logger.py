from config import Config
import logging

class Logger():
    def __init__(self):
        file=Config().log
        logging.basicConfig(format="%(asctime)s %(message)s", filename=file, level=logging.DEBUG)
        lines=sum(1 for line in open(file))
        if lines >= Config().loglines:
            logfile=open(file)
            loglines=logfile.readlines()
            logfile.close()
            logfile=open(file, "w")
            i=0
            for line in loglines:
                if i > (lines-Config().loglines):
                    logfile.write(line)
                i=i+1
    def startup(self):
        logging.info("Database: " + Config().db)
        logging.info("Source-URL: " + Config().url)
    def log(self, log):
        logging.info(log)
