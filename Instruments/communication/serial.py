# Instruments/communication/serial.py

class SerialInterface:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate

    def connect(self):
        print(f"Connecting via Serial to port {self.port} with baudrate {self.baudrate}")
    
    def disconnect(self):
        print(f"Disconnecting Serial connection at port {self.port}")
