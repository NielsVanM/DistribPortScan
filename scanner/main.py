import json

from flask import Flask, request
from requests import post

from jobqueue import Job, Queue
import threading

address = "localhost"
port = 3400

resp = post("http://localhost:5000/register_node", data={"address": address, "port": port})

q = Queue()

app = Flask("ScanNode")

@app.route("/register_job", methods=["POST"])
def RegisterJob():
    print(
        request.json
    )
    j = Job(
        request.json["callback"],
        request.json["job"]["ip"],
        request.json["job"]["port"]
    )

    q.addJob(j)

    return "OK"

@app.route("/status", methods=["GET"])
def Status():
    return json.dumps(
        [j.toJson() for j in q.q]
    )

def ScanRoutine(q):

    while True:
        pass

    pass

threading.Thread(target=ScanRoutine, args=(q,)).start()

app.run(port=port)