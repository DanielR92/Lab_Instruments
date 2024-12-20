# Instruments/communication/serial.py
from pymodbus.client import ModbusSerialClient

class SerialInterface:

    def __init__(self, port, baudrate, protocol=''):
        self.port = port
        self.baudrate = baudrate
        
        # Stelle sicher, dass die Adresse vorhanden ist
        if self.port is None:
            raise ValueError("Port muss angegeben werden.")
                
        if protocol == 'rtu':
            self.rm = ModbusSerialClient(port=self.port, baudrate=self.baudrate)
        else:
            self.rm = SerialInterface(port=port, baudrate=baudrate)  # ResourceManager instanziieren
        
        self.device = None  # Gerät wird noch nicht verbunden
        
        print(f"RTU Interface mit Port {self.port} erstellt.")

    def connect(self):
        self.rm.connect()
        print(f"Connecting via Serial to port {self.port} with baudrate {self.baudrate}")
    
    def disconnect(self):
        self.rm.close()
        print(f"Disconnecting Serial connection at port {self.port}")
        
    def reset(self):
        self.rm.reset()
        print(f"Reset Serial connection at port {self.port}")
        
    def write_register(self, address, data, unit):
        self.rm.write_register(address, data, unit)
        
    def read_register(self, address):
        return self.rm.read_register(address)