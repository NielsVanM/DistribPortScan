import threading
import time

from jobs import ScanJobManager
from node_manager import NodeManager


nm = NodeManager()
scm = ScanJobManager()

def APIThread():
    nm.StartRegistrationListener()

def CreateJobThread():
    scm.GenerateJobs()

def SpreadJobThread():
    while True:
        nm.SpreadJobs(scm)
        time.sleep(10)

threading.Thread(target=APIThread).start()
threading.Thread(target=CreateJobThread).start()
threading.Thread(target=SpreadJobThread).start()

while True:
    try:
        time.sleep(60)
    except:
        break