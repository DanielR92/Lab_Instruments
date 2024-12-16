# Instruments/communication/tcpip.py

class TCPIPInterface:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect(self):
        print(f"Connecting via TCP/IP to {self.ip}:{self.port}")
    
    def disconnect(self):
        print(f"Disconnecting TCP/IP connection at {self.ip}:{self.port}")
