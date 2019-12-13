import threading
import time

from jobs import ScanJobManager
from node_manager import NodeManager


def APIThread():
    nm = NodeManager()

    nm.StartRegistrationListener()

def JobThread():
    scm = ScanJobManager()
    scm.GenerateJobs()


threading.Thread(target=APIThread).start()
# threading.Thread(target=JobThread).start()

while True:
    try:
        time.sleep(60)
    except:
        break