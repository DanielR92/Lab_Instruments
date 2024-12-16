import pyvisa
import sys

class GPIBInterface:
    def __init__(self, **kwargs):
        # Extrahiere die Adresse aus den übergebenen Parametern
        self.address = kwargs.get('address')
        
        # Stelle sicher, dass die Adresse vorhanden ist
        if self.address is None:
            raise ValueError("GPIB-Adresse muss angegeben werden.")
        
        # Initialisiere den VISA ResourceManager
        self.rm = pyvisa.ResourceManager()  # ResourceManager instanziieren
        self.device = None  # Gerät wird noch nicht verbunden
        print(f"GPIB Interface mit Adresse {self.address} erstellt.")

    def connect(self):
        """
        Stellt eine Verbindung zum GPIB-Gerät her.
        """
        try:
            # Verbindungsaufbau zum Gerät über die GPIB-Adresse
            self.device = self.rm.open_resource(f"GPIB::{self.address}::INSTR")
        except pyvisa.VisaIOError as e:
            sys.exit(f"Fehler beim Verbinden mit dem GPIB-Gerät: {e}")
        except Exception as e:
            print(f"Ein unbekannter Fehler ist aufgetreten: {e}")

    def disconnect(self):
        """
        Trennt die Verbindung zum GPIB-Gerät.
        """
        if self.device:
            self.device.close()
        else:
            print("Keine aktive Verbindung zum Gerät.")

    def reset(self):
        """
        Setzt das GPIB-Gerät zurück.
        """
        if self.device:
            self.device.write("*RST")  # Sende den RESET-Befehl an das Gerät
        else:
            print("Keine aktive Verbindung zum Gerät.")

    def query(self, command):
        if self.device:
            try:
                self.device.write(command)  # Sende den Befehl an das Gerät
                result = self.device.read()  # Lese das Ergebnis der Messung
                return result
            except pyvisa.VisaIOError as e:
                print(f"Fehler query: {e}")
        else:
            print("Keine aktive Verbindung zum Gerät.")
        return None

    def write(self, command):
        self.device.write(command)  # Sende den Befehl an das Gerät
