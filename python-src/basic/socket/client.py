import socket
import time
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

    def connect(self, retry_attempts=3, delay_between_retries=5):
        if self._clt:
            return
        self._clt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for attempt in range(retry_attempts):
            try:
                self._clt.connect((self.ipaddr, self.port))
                self.connected = True
                print("Connected to server.")
                break  
            except Exception as e:
                self.connected = False
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retry_attempts - 1:
                    print(f"Retrying in {delay_between_retries} seconds...")
                    time.sleep(delay_between_retries)
                else:
                    print("Could not connect to the server after several attempts.")
                    self._clt = None

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
