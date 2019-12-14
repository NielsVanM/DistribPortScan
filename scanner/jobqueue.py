

class Job():
    def __init__(self, callback, ip, port):
        self.callback = callback
        self.ip = ip
        self.port = port
    
    def toJson(self):
        return {
            "callback": self.callback,
            "ip": self.ip,
            "port": self.port,
        }

class Queue():
    
    q = []

    def addJob(self, job):
        self.q.append(job)




