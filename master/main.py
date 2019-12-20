import threading
import time

from jobs import ScanJobManager
from node_manager import NodeManager


scm = ScanJobManager()
scm.NewJob(addr=("178.62.120.181", 80))

nm = NodeManager(scm)

def APIThread():
    nm.StartRegistrationListener()

def CreateJobThread():
    scm.GenerateJobs()

def SpreadJobThread():
    while True:
        nm.SpreadJobs(scm)
        time.sleep(10)

t_api = threading.Thread(target=APIThread)
t_api.start()

t_create_job = threading.Thread(target=CreateJobThread)
t_create_job.start()

t_spread_job = threading.Thread(target=SpreadJobThread)
t_spread_job.start()

t_api.join()
t_create_job.join()
t_spread_job.join()

while True:
    try:
        time.sleep(60)
    except:
        break