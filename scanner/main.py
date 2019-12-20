import json

from flask import Flask, request
from requests import post
from requests import ConnectionError

from jobqueue import Job, Queue
from scanner import MultiScanner

address = "localhost"
port = 3400

try:
    resp = post("http://localhost:5000/register_node", data={"address": address, "port": port})
except ConnectionError:
    # exit(-1)
    pass

q = Queue()
scanner = MultiScanner()

app = Flask("ScanNode")

@app.route("/register_job", methods=["POST"])
def RegisterJob():
    # j = Job(
    #     request.json["callback"],
    #     request.json["job"]["ip"],
    #     request.json["job"]["port"]
    # )

    # q.addJob(j)

    scanner.AddScan(
        request.json["job"]["ip"],
        request.json["job"]["port"],
        request.json["callback"]
    )

    return "OK"

@app.route("/status", methods=["GET"])
def Status():
    return json.dumps(
        [j.toJson() for j in q.q]
    )


app.run(port=port)