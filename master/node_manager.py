from flask import Flask, request
import json
import uuid
import requests
import jobs

class Node():
    def __init__(self, ip, port, _id=None):
        self.ip = ip
        self.port = port

        if _id == None:
            _id = str(uuid.uuid4())
    

    def SendJob(self, job):
        data = {
            "job": job,
            "callback": f"http://127.0.0.1:5000/cb/job?id={job.id}"
        }

        resp = requests.post(f"http://{self.ip}:{self.port}", data=json.dumps(data))
        if resp.status_code != 200:
            return None

        job.status = jobs.ASSINGED


class NodeManager():
    node_list = []

    def RegisterNode(self, ip, port):
        self.node_list.append({
            "ip": ip,
            "port": port
        })

    def _httpRegisterNode(self):
        return "K"
        self.RegisterNode(
            request.form["address"],
            request.form["port"]
        )

        return "Success"
    
    def _httpStatus(self):
        return json.dumps(self.node_list)

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

        