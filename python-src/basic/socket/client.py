import socket
from basic.payload import builder

class BasicClient(object):
    def __init__(self, name, ipaddr="127.0.0.1", port=2000):
        self._clt = None
        self.name = name
        self.ipaddr = ipaddr
        self.port = port
        self.group = "public"
        self.connected = False  

        if not self.ipaddr:
            raise ValueError("IP address is missing or empty")
        if not self.port:
            raise ValueError("Port number is missing")
        self.connect()

    def __del__(self):
        self.stop()

    def stop(self):
        if self._clt:
            self._clt.close()
        self._clt = None
        self.connected = False

    def connect(self):
        if self._clt:
            return
        addr = (self.ipaddr, self.port)
        self._clt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._clt.connect(addr)
            self.connected = True
        except Exception as e:  
            print(f"Could not connect to server: {e}")
            self.connected = False

    def join(self, group):
        self.group = group

    def sendMsg(self, text):
        if not self.connected:
            raise RuntimeError("No connection to server exists")
        print(f"sending to group {self.group} from {self.name}: {text}")
        bldr = builder.BasicBuilder()
        m = bldr.encode(self.name, self.group, text)
        self._clt.send(bytes(m, "utf-8"))

    def groups(self):
        # Placeholder for future implementation
        pass

    def getMsgs(self):
        # Placeholder for future implementation
        pass

if __name__ == '__main__':
    clt = BasicClient("full_stack_alchemists", "127.0.0.1", 2000)
    while True:
        m = input("Enter message: ")
        if m == '' or m.lower() == 'exit':
            break
        clt.sendMsg(m)
