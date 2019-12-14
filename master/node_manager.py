import json
import random
import uuid

import requests
from flask import Flask, request

import jobs


class Node():
    def __init__(self, ip, port, _id=None):
        self.ip = ip
        self.port = port

        if _id == None:
            self._id = str(uuid.uuid4())
        else:
            self._id = _id  

    def SendJob(self, job):
        data = {
            "job": job.toJson(),
            "callback": f"http://127.0.0.1:5000/cb/job?id={job._id}"
        }

        resp = requests.post(f"http://{self.ip}:{self.port}/register_job", json=data)
        if resp.status_code != 200:
            return None

        job.status = jobs.ASSIGNED

    def toJson(self):
        return {
            "ip": self.ip,
            "port": self.port,
            "_id": self._id
        }


class NodeManager():
    node_list = []

    def RegisterNode(self, ip, port):
        self.node_list.append(
            Node(ip, port)
        )

    def _httpRegisterNode(self):
        self.RegisterNode(
            request.form["address"],
            request.form["port"]
        )

        return "Success"
    
    def _httpStatus(self):
        return json.dumps(
            [node.toJson() for node in self.node_list]
        )

    def StartRegistrationListener(self, routes=[]):
        self.app = Flask(import_name="ScanMaster")

        routes += [
            # (URL, Function to exec, [Methods])
            ("/register_node", self._httpRegisterNode, ["POST",]),
            ("/status", self._httpStatus, ["GET",])
        ]

        for r in routes:
            self.app.add_url_rule(
                r[0],
                view_func = r[1],
                methods=r[2]
            )

        self.app.run()

    def SpreadJobs(self, scanManager):
        job_list = scanManager.GetPendingJobs()

        print(f"Spreading {len(job_list)} jobs to {len(self.node_list)} nodes at random.")

        for job in job_list:
            print(job)
            if len(self.node_list) < 1:
                return

            random.choice(self.node_list).SendJob(job)
