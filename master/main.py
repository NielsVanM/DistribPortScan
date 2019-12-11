import threading
import time

from jobs import ScanJobManager
from node_manager import RunAPI

scm = ScanJobManager()

threading.Thread(target=RunAPI).start()
threading.Thread(target=scm.GenerateJobs).start()

while True:
    try:
        time.sleep(60)
    except:
        break