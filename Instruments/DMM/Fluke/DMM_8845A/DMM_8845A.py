import importlib
import os

from Instruments.DMM.Fluke.DMM_8845A.constants import MeasurementMode
from Instruments.DMM.Fluke.DMM_8845A.constants import math_function_matrix

class Device:
    """Repräsentiert das Fluke 8845A Multimeter."""
    
    def __init__(self, interface_type, interface_info, ID):
        self.ID = ID
        self.constants = self._load_constants()  # Lade die constants.py automatisch

        # Verwende das interface_info Dictionary für den Aufbau der Schnittstelle
        if interface_type == "GPIB":
            from Instruments.communication.gpib import GPIBInterface
            self.interface = GPIBInterface(address=interface_info.get('address'))
        elif interface_type == "Serial":
            from Instruments.communication.serial import SerialInterface
            self.interface = SerialInterface(**interface_info)
        elif interface_type == "TCPIP":
            from Instruments.communication.tcpip import TCPIPInterface
            self.interface = TCPIPInterface(**interface_info)
        else:
            raise ValueError(f"Unbekannter Schnittstellentyp: {interface_type}")
            return;
        self.connect()

    def measure(self, mode: MeasurementMode):
        """
        Führt eine Messung durch.
        
        :param mode: Enum-Wert aus MeasurementMode, z. B. VOLTAGE_DC.
        :return: Messwert als String.
        """
        if not isinstance(mode, MeasurementMode):
            raise ValueError("Ungültiger Modus für Messung.")
        
        scpi_command = f"MEAS:{mode.value}?"
        result = self.interface.query(scpi_command)
        print(f"Messwert für {mode.name}: {result}")
        return result
    
    def configure_range(self, mode: MeasurementMode, range_value: float):
        """
        Konfiguriert den Messbereich.

        :param mode: Enum-Wert aus MeasurementMode, z. B. VOLTAGE_DC.
        :param range_value: Messbereichswert (z. B. 10.0 für 10 V).
        """
        if not isinstance(mode, MeasurementMode):
            raise ValueError("Ungültiger Modus für RANGE.")
        
        scpi_command = f"CONF:{mode.value} {range_value}"
        self.interface.write(scpi_command)
        print(f"Messbereich für {mode.name} auf {range_value} konfiguriert.")

    def set_autozero(self, state: MeasurementMode):
        """
        Aktiviert oder deaktiviert den Autozero-Modus.

        :param state: ONOFF-Enum-Wert (ON oder OFF).
        """
        scpi_command = f"SENSe:ZERO:AUTO {state.value}"
        self.interface.write(scpi_command)
        print(f"Autozero wurde auf {state.name} gesetzt.")

    def set_average(self, count: int):
        """
        Konfiguriert den Mittelungsmodus.

        :param count: Anzahl der Mittelungsdurchläufe.
        """
        if count < 1 or count > 100:
            raise ValueError("Anzahl der Mittelungen muss zwischen 1 und 100 liegen.")
        
        scpi_command = f"SENSe:AVERage:COUNt {count}"
        self.interface.write(scpi_command)
        print(f"Anzahl der Mittelungen auf {count} gesetzt.")

    # Lädt automatisch eine Datei namens 'constants.py' aus demselben Verzeichnis.
    def _load_constants(self):
        # Hole den Pfad des aktuellen Moduls
        current_module = __name__
        module_name = f"{current_module.rsplit('.', 1)[0]}.constants"
        
        try:
            # Versuche, das Modul 'constants' zu importieren
            constants_module = importlib.import_module(module_name)
            print(f"'constants.py' erfolgreich geladen aus {module_name}")
            return constants_module
        except ModuleNotFoundError:
            print(f"Keine 'constants.py' im Modul {module_name} gefunden.")
            return None
    
    def set_frequency_aperture(self, aperture: float):
        """
        Setzt die Aperture-Zeit für Frequenzmessungen.

        :param aperture: Aperture-Zeit in Sekunden.
        """
        if aperture <= 0:
            raise ValueError("Aperture muss positiv sein.")
        
        scpi_command = f"FREQ:APER {aperture}"
        self.interface.write(scpi_command)
        print(f"Aperture-Zeit auf {aperture} Sekunden gesetzt.")

    def connect(self):
        """Verbindet mit dem Gerät."""
        self.interface.connect()
        print(f"Verbinde mit Gerät über {self.interface} mit ID {self.ID}.")

    def disconnect(self):
        """Trennt die Verbindung zum Gerät."""
        self.interface.disconnect()
        print("Verbindung zum Gerät getrennt.")

    def reset(self):
        """Setzt das Gerät zurück."""
        self.interface.reset()
        print("Gerät zurückgesetzt.")

    # _ underscore marks function to private
    # Perform self-test. Returns “0” if the test succeeds, “1” if the test fails.
    def self_test(self):
        if not self.interface.write("*TST"):
            msg = "Ok"
        else:
            msg = "Error!"
        print("Selbst Test: " + msg)

    # Setzt den Modus des Geräts.
    def set_mode(self, mode):
        #if isinstance(mode, Enum):

        self.interface.write(mode)
        print(f"Modus auf {mode} gesetzt.")

    # Führt eine Messung durch
    def _get(self, mode):
        if isinstance(mode, MeasurementMode):
            mode = mode.value
        return self.interface.query("MEAS:" + mode + "?")  # Übergabe des Befehls an das Interface  

    def get_VolatgeDC(self):
        return self._get(MeasurementMode.VOLTAGE_DC)
    
    def get_VolatgeDC_Ratio(self):
        return self._get(MeasurementMode.VOLTAGE_DC_RATIO)
    
    def get_VolatgeAC(self):
        return self._get(MeasurementMode.VOLTAGE_AC)
    
    def get_CurrentDC_mA(self):
        self.set_mode()
        return self._get(MeasurementMode.CURRENT_DC)
    
    def get_CurrentDC_10A(self):
        self.set_mode()
        return self._get(MeasurementMode.CURRENT_DC)

    def get_CurrentAC(self):
        return self._get(MeasurementMode.CURRENT_AC)

    def get_Resistor2W(self):
        return self._get(MeasurementMode.TWO_WIRE_RESISTANCE)

    def get_Resistor4W(self):
        return self._get(MeasurementMode.FOUR_WIRE_RESISTANCE)

    def get_Continuity(self):
        return self._get(MeasurementMode.CONTINUITY)

    def get_Diode(self):
        return self._get(MeasurementMode.DIODE)
    
    def _setAperture(self, cmd, value):
        cmd += ":APER " + str(value)
        self.set_mode(cmd)

    def get_Frquency(self, aperture):
        self._setAperture("FREQ", aperture.value)
        return self._get(MeasurementMode.FREQUENCY)
    
    def sense_measure(self, cmd):
        return self.interface.query(cmd)  
    
    def get_ROUTE(self):
        return self.interface.query("ROUT:TERM?")  
    
    def set_MATH(self, mode):
        if(mode):
            self.interface.write("CALC:STAT " + MeasurementMode.ON)
        else:
            self.interface.write("CALC:STAT " + MeasurementMode.OFF)
            
    # Prüft, ob eine gegebene Kombination von Math-Funktion und Meter-Funktion erlaubt ist.
    def is_combination_allowed(self, math_function, meter_function):

        # Prüfen, ob die Eingaben gültig sind
        if math_function not in math_function_matrix:
            return f"Ungültige Math-Funktion: {math_function}"
        if meter_function not in math_function_matrix[math_function]:
            return f"Ungültige Meter-Funktion: {meter_function}"
        
        # Rückgabe des Werts aus der Matrix
        result = math_function_matrix[math_function][meter_function]
        return f"Erlaubt: {result}"
