import importlib
import os

from Instruments.communication.gpib import GPIBInterface
from Instruments.communication.serial import SerialInterface
from Instruments.communication.tcpip import TCPIPInterface

class Instruments:
    """Zentrale Verwaltung der Geräte und Schnittstellen"""

    def __init__(self):
        self.devices = {}  # Speichert alle Geräteklassen
        self.interfaces = {
            "GPIB": GPIBInterface,
            "Serial": SerialInterface,
            "TCPIP": TCPIPInterface
        }  # Verfügbare Schnittstellen
        self._load_devices()

    def _load_devices(self):
        """Lädt alle Geräte dynamisch aus dem 'DMM' Verzeichnis"""

        # Basisverzeichnis, z. B. das Verzeichnis des aktuellen Skripts
        base_dir = os.path.dirname(os.path.realpath(__file__))

        if not os.path.isdir(base_dir):
            print(f"Das Verzeichnis {base_dir} existiert nicht.")
            return

        # Liste, um die passenden Verzeichnisse zu speichern
        directories = []

        for root, _, files in os.walk(base_dir):
            # Prüfe, ob eine '__init__.py' vorhanden ist, um das Verzeichnis als Modul zu kennzeichnen
            if '__init__.py' in files:
                # Generiere den relativen Modulpfad, z. B. 'DMM.Fluke.DMM_8845A'
                relative_path = os.path.relpath(root, start=os.path.dirname(base_dir))
                module_name = relative_path.replace(os.sep, ".")  # Pfad zu Modul konvertieren

                try:
                    # Modul dynamisch importieren
                    module = importlib.import_module(module_name)
                    device_class = getattr(module, 'Device', None)  # Sucht nach der Device-Klasse
                    if device_class:
                        # Modulname als Schlüssel, Klasse als Wert speichern
                        self.devices[module_name] = device_class
                        print(f"Gerät {module_name} erfolgreich geladen.")
                except ModuleNotFoundError as e:
                    print(f"Modul {module_name} konnte nicht geladen werden: {e}")
                except Exception as e:
                    print(f"Fehler beim Laden des Moduls {module_name}: {e}")
    
    def get_device(self, device_name):
        """Gibt eine Instanz des Geräts zurück."""
        device_class = self.devices.get(device_name)
        if device_class:
            return device_class
        else:
            raise ValueError(f"Gerät {device_name} nicht gefunden.")

    def get_interface(self, interface_name, *args, **kwargs):
        """Erstellt eine Instanz der gewünschten Schnittstelle."""
        interface_class = self.interfaces.get(interface_name)
        if interface_class:
            return interface_class(*args, **kwargs)
        else:
            raise ValueError(f"Schnittstelle {interface_name} nicht verfügbar.")