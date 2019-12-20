import threading
import time
import socket
import re
import requests
from requests import ConnectionError

class MultiScanner():
    def __init__(self):
        self.queue_list = []
        self.scan_list = []
        self.t_list = []

        # Start scan schedule
        self.t_schedule = threading.Thread(target=self.ScanScheduler)
        self.t_schedule.start()
        # self.t_schedule.join()

        self.scan_types = Scan.__subclasses__()

        print("The following protocol scanners have been loaded:")
        print(
            "{0}{1}".format(
                "\t",
                "\n\t".join([st.__name__ for st in self.scan_types])
                )
            )
        
        print("Started Scan Thread")
    
    def AddScan(self, ip, port, callbackURL):
        self.queue_list.append(
            (ip, port, callbackURL)
        )

    def ScanScheduler(self):
        while True:
            if len(self.queue_list) < 1:
                time.sleep(10)
                continue
            
            print("Starting scans")

            for i, scan in enumerate(self.queue_list):
                t_scan = threading.Thread(target=self.ScanTarget, args=(scan[0], scan[1], scan[2]))
                t_scan.start()

                self.queue_list.pop(i)
                self.scan_list.append(scan)

                self.t_list.append(
                    t_scan
                )

    def ScanTarget(self, ip, port, callbackURL):
        for s in self.scan_types:
            st = s()

            sock = socket.socket()
            try:
                sock.connect((ip, port))
            except:
                self.ResultCallback(callbackURL, {"status": "failed"})
                return
            
            sock.send(
                st.GetRequestFormat({"ip": ip, "port": port})
            )

            data = sock.recv(2048)
            if st.VerifyResponse(data.decode()):
                sock.close()

                self.ResultCallback(callbackURL, {"status": "success", "raw_resp": data.decode(), "protocol": st.GetName()})

                return
            sock.close()
        
        self.ResultCallback(callbackURL, {"status": "failed"})

    def ResultCallback(self, url, data):
        try:
            res = requests.post(
                url,
                json=data
            )
        except requests.ConnectionError:
            print("Remote server unavailable")
            exit(-1)

        if res.status_code == 200:
            print(f"Finished {url}")
            return

        print("Failed to report status back to caller")

class Scan():
    def GetRequestFormat(self):
        raise NotImplementedError()

    def VerifyResponse(self):
        raise NotImplementedError()

class HTTPScan(Scan):
    def GetRequestFormat(self, data):
        if type(data) is not dict:
            raise ValueError("Provided data is not a dictionary")
    
        return f"""GET / HTTP/1.1\nHost: {data["ip"]}:{data["port"]}\n\n""".encode()
    
    def VerifyResponse(self, data):
        if re.match("HTTP\/[1-2]\.[0-2]", data):
            return True
        return False
    
    def GetName(self):
        return "HTTP"