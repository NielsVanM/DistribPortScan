import json
import time
from ipaddress import IPv4Address
from random import getrandbits, randint
from uuid import uuid4
from flask import escape

PENDING = "Pending"
ASSIGNED = "Assigned"
FINISHED = "Finished"
ERROR = "Error Occured"


class ScanJob():
    def __init__(self, ip, port):
        self._id = uuid4().__str__()
        self.status = PENDING
        self.ip = ip
        self.port = port
        self.raw_data = None
        self.protocol = None
    
    def toJson(self):
        return {
            "status": self.status,
            "ip": self.ip,
            "port": self.port,
            "raw_data": self.raw_data,
            "protocol": self.protocol
        }

class ScanJobManager():
    limit = 10
    _job_list = {}

    def GenerateJobs(self):
        while True:
            self.NewJob()
            time.sleep(1)

    def NewJob(self, addr=None):
        if len(self.GetUnfinishedJobs()) > self.limit:
            return

        if addr == None:
            sj = ScanJob(
                str(IPv4Address(getrandbits(32))),
                randint(1, 65535)
            )
        else:
            sj = ScanJob(
                addr[0], addr[1]
            )
        
        self._job_list[sj._id] = sj

        print(f"Created Job {sj._id} for {sj.ip}:{sj.port}")

        return sj._id
        
    def GetStatus(self, _id):
        return self._job_list[_id].status

    def GetUnfinishedJobs(self):
        lst = []
        lst += self.GetPendingJobs()
        lst += self.GetAssignedJobs()
        return lst
    
    def GetPendingJobs(self):
        return [value for key,value in self._job_list.items() if value.status == PENDING]
    
    def GetAssignedJobs(self):
        return [value for key,value in self._job_list.items() if value.status == ASSIGNED]

    def GetFinishedJobs(self):
        return [value for key,value in self._job_list.items() if value.status == FINISHED]
    
    def GetErroredJobs(self):
        return [value for key,value in self._job_list.items() if value.status == ERROR]

    def SetJobStatus(self, job_id, status):
        try:
            self._job_list[job_id].status = status
        except KeyError:
            print(f"Failed to find job with ID {job_id}")
        
    def SetJobData(self, job_id, data):
        try:
            self._job_list[job_id].raw_data = data
        except KeyError:
            print(f"Failed to find job with ID {job_id}")

    def SetJobProtocol(self, job_id, prot):
        try:
            self._job_list[job_id].protocol = prot
        except KeyError:
            print(f"Failed to find job with ID {job_id}")