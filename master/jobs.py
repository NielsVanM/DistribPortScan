import json
import time
from ipaddress import IPv4Address
from random import getrandbits, randint
from uuid import uuid4

PENDING = "Pending"
ASSIGNED = "Assigned"
FINSHED = "Finished"
ERROR = "Error Occured"


class ScanJob():
    def __init__(self, ip, port):
        self.id = uuid4().__str__()
        self.status = PENDING
        self.ip = ip
        self.port = port
    
    def toJson(self):
        return json.dumps({
            "status": self.status,
            "ip": self.ip,
            "port": self.port
        })

class ScanJobManager():
    limit = 10
    _job_list = {}

    def GenerateJobs(self):
        while True:
            self.NewJob()
            time.sleep(1)

    def NewJob(self):
        if len(self.GetPendingJobs()) > self.limit:
            return

        sj = ScanJob(
            str(IPv4Address(getrandbits(32))),
            randint(1, 65535)
        )

        self._job_list[sj.id] = sj

        print(f"Created Job {sj.id} for {sj.ip}:{sj.port}")

        return sj.id

    def GetStatus(self, id):
        return self._job_list[id].status
    
    def GetPendingJobs(self):
        return [value for key,value in self._job_list.items() if value.status == PENDING]
