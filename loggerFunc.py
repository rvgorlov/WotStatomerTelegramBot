import config
from datetime import datetime

def log(loginfo):
    if config.DEBUG:
        now = datetime.now()
        now = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
        loginfo = "(" + now + ") ---" + loginfo
        print("-- " + str(loginfo))
    else:
        pass
