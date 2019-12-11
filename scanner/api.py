from flask import Flask

api = Flask(import_name="ScanNode")

@api.route("/register_node/{uuid}")
def RegisterNode():
    pass
