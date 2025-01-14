import importlib
import os
from time import sleep


class Device:
    """Repräsentiert das FATEN VanCryst™ VS481C."""

    @property
    def name(self):
        """Gibt den Namen zurück (read-only)."""
        return self._name
    
    def __init__(self, interface_type, interface_info, baudrate=19200):
        print("[Init:Start]-----------------------------")
        self._port          = interface_info['port']
        self._manufacturer  = None
        self._model         = None
        self._serialnumber  = None
        self._SWversion     = None
        self._SWDispVersion = None

        self._hdmi_ports    = 4 # max. 4 HDMI-Ports
        self._priority      = 0
        self._hdmi_output   = 0 # Turn on the output port / 0 = off, 1 = on
        self._hdmi_auto     = 0 # Auto switch / 0 = off, 1 = on Disable the switch mode and the VS481C does not switch ports automatically
        self._hdmi_POD      = 0 # Power On Detect / 0 = off, 1 = on

        # Verwende das interface_info Dictionary für den Aufbau der Schnittstelle
        if interface_type == "Serial":
            from Instruments.communication.serial import SerialInterface
            interface_info.setdefault('baudrate', baudrate)
            self._client = SerialInterface(**interface_info)
        else:
            raise ValueError(f"Unbekannter Schnittstellentyp: {interface_type}")

        self._connect()
        self.Identification()
        print("[Init:Done]-----------------------------")

    def __exit__(self):
        print("Delete Module 'VS481C' ... ", end=" ")
        self.disconnect()
        print(" ... done.")

    def Identification(self):
        ''' Set the device identification. '''

        IDN = self.identification()
        self._manufacturer  = "ATEN"
        self._model         = "VanCryst™ VS481C"
        self._serialnumber  = None
        self._SWversion     = None
        return self
    
    def write(self, command):
        ''' Write a command to the device. '''
        self._client.write(command + '\n')

    def _connect(self):
        """Verbindet mit dem Gerät."""
        self._client.baudrate = 19200
        self._client.terminator = '\r'
        self._client.connect()

    def disconnect(self):
        """Trennt die Verbindung zum Gerät."""
        self._client.disconnect()

    def Identification(self):
        """Identifikation des Geräts lesen und speichern."""
        self._client.client.flush()  # Puffer leeren
        self.write("read")  # Befehl senden

        # Daten aus der Schnittstelle lesen
        raw_idn = self._client.client.readlines()

        # Sicherstellen, dass Daten empfangen wurden
        if not raw_idn:
            raise IOError("Keine Antwort vom Gerät erhalten.")

        # Bytes-Daten in Strings konvertieren und bereinigen
        idn = [line.decode('utf-8').strip() for line in raw_idn]

        # Überprüfen, ob die Antwort gültig ist
        if "Command OK" in idn[0]:
            self._hdmi_output = int(idn[1].replace("Input: port ", ""))

            if idn[2].endswith("ON"):
                self._hdmi_output = True
            else:
                self._hdmi_output = False

            self._priority = int(idn[3].replace("Mode: Priority", 1))

            if idn[4].endswith("ON"):
                self._hdmi_POD = True
            else:
                self._hdmi_POD = False

            self._SWversion = idn[5].replace("F/W: ", "")

            print(f"Firmware-Version: {self._SWversion}")
            return self
        else:
            raise ValueError("Ungültige Antwort vom Gerät: 'Command OK' fehlt.")
    
    def set_output(self, flag):
        if not isinstance(flag, bool):
            raise ValueError("Der Modus muss eine boolean sein.")

        self._hdmi_output = flag

        if flag:
            self._client.write(f"sw on")
        else:
            self._client.write(f"sw off")

        print(f"Output auf {flag} gesetzt.")      

    # Setzt den neuen Input des Geräts.
    def set_input(self, mode):
        if not isinstance(mode, int):
            raise ValueError("Der Modus muss eine ganze Zahl sein.")
        
        if not mode:
            self.set_output(False)
            return

        if not self._hdmi_output:
            self.set_output(True)

        self._client.write(f"sw i{mode:02}")
        print(f"Modus auf {mode} gesetzt.")

  
    def set_POD(self, mode=False):
        if not isinstance(mode, bool):
            raise ValueError("Der Modus muss eine boolean sein.")
        
        self._hdmi_POD = mode

        if self._hdmi_POD:
            self._client.write(f"swmode pod on")
        else:
            self._client.write(f"swmode pod off")

        print(f"POD auf {self._hdmi_POD} gesetzt.")

    def disable_switch(self):        
        self._hdmi_auto = False
        self._client.write(f"swmode off")

        print(f"Auto-Switch auf {self._hdmi_auto} gesetzt.")

    def set_priotity(self, port):
        if not isinstance(port, int):
            raise ValueError("Der Port muss eine ganze Zahl sein.")
        
        self._client.write(f"swmode i{port:02} priority")
        print(f"Priorität auf Port {port} gesetzt.")

    if __name__ == "__main__":
        print("This module is not intended to run standalone.")
        print("Please import it in your main program.")
        print("Exiting...")
        exit(1)