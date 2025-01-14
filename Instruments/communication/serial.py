# Instruments/communication/serial.py
import serial  # pySerial
from pymodbus.client import ModbusSerialClient

class SerialInterface:

    def __init__(self, port, baudrate, protocol=''):
        self.port = port
        self.baudrate = baudrate
        self.protocol = protocol
        self.client = None  # Platzhalter für Modbus- oder pySerial-Verbindung
            
        # Stelle sicher, dass die Adresse vorhanden ist
        if self.port is None:
            raise ValueError("Port muss angegeben werden.")
        
        if protocol == 'rtu':  # Modbus RTU verwenden
            self.client = ModbusSerialClient(
                port=self.port,
                baudrate=self.baudrate,
                method='rtu',
                stopbits=1,
                bytesize=8,
                parity='N',
                timeout=1
            )
            print(f"Modbus RTU-Interface mit Port {self.port} erstellt.")
        elif protocol == 'serial' or protocol == '':  # Standard pySerial verwenden
            self.client = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                timeout=1
            )
            print(f"Standard-Serial-Interface mit Port {self.port} erstellt.")
        else:
            raise ValueError(f"Unbekanntes Protokoll: {protocol}")
    

    def connect(self):
        if self.protocol == 'rtu':
            self.client.connect()

        print(f"Connecting via Serial to port {self.port} with baudrate {self.baudrate}")

    def disconnect(self):
        self.client.close()
        print(f"Disconnecting Serial connection at port {self.port}")
        
    def reset(self):
        self.client.reset()
        print(f"Reset Serial connection at port {self.port}")
        
    def write_register(self, address, data, slave):
        self.client.write_register(address, data, slave)
        
    def read_register(self, address):
        return self.client.read_register(address)
    
    def write(self, data):
        data = data + '\r' if not data.endswith('\r') else data
        self.client.write(data.encode('utf-8') if isinstance(data, str) else data)