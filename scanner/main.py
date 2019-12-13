from flask import Flask
from requests import post

address = "localhost"
port = 3400

resp = post("http://localhost:5000/register_node", data={"address": address, "port": port})

