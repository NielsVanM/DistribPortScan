from flask import Flask, request
import json



def RunAPI():
    print("starting server")
    app.run()

app = Flask(import_name="ScanMaster")

nodes = []

@app.route("/register_node", methods=["POST"])
def RegisterNode():
    d = request.form

    nodes.append({
        "address": d["address"],
        "port": d["port"],
    })

    return "Success"

@app.route("/status")
def Status():
        return json.dumps(nodes)
