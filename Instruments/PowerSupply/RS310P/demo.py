# demo.py
import logging
from Instruments.instruments import Instruments

logger = logging.getLogger(__name__)

# Instanziere die Klasse
instruments = Instruments()

try:
    powersupply_device_class = instruments.get_device('Instruments.PowerSupply.RS310P')
    powersupply_device = powersupply_device_class(interface_type="Serial", interface_info={'port': "COM18"})

    powersupply_device.setLConfig(volt=10, current=1, OVP=15, OCP=0.5, OPP=12)

    powersupply_device.setCurrentLimit(1)       # Setzt den Strom auf 1A
    powersupply_device.setVoltage(19.0)         # Setzt die Spannung auf 19V
    powersupply_device.setOutput(1)             # Schaltet die Ausgangsspannung ein / 0 - aus
    powersupply_device.setOverVoltageP(20.0)    # Setzt die Oberspannungsschutzspannung auf 20V
    powersupply_device.setOverCurrentP(1.1)     # Setzt den Überstromschutz auf 1.1A
    powersupply_device.setOverPowerP(20.0)      # Setzt den Überlastschutz auf 20W
    powersupply_device.setBuzzer(1)             # Schaltet den Summer ein / 0 - aus
    
    powersupply_device.setOutput(1) 
    voltage = powersupply_device.get_actual_voltage()     # Liest die aktuelle Ausgangsspannung
    output = powersupply_device.getOutput()              # Liest den Ausgangszustand
    
    model = powersupply_device.getModel()               # Liest das Modell
    state = powersupply_device.getOutputStats()         # Liest die Ausgangsstatistiken (Volt, Ampere, Watt)
    tVolt = powersupply_device.getTargetVolts()         # Liest die Zielspannung
    limit = powersupply_device.getCurrentLimit()        # Liest den Strombegrenzungswert

    protectValue = powersupply_device.getProtectionValues()    # Liest die Schutzspannungen (OVP, OCP, OPP)
    protectState = powersupply_device.getProtectionState()     # Liest den Schutzstatus (1 if protection mode is enabled, else 0)

    buzzer= powersupply_device.getBuzzer()              # Liest den Summerzustand

except Exception as e:      # works on python 3.x
    logger.error('Error: %s', repr(e))

finally:
    # Gerät trennen
    powersupply_device.disconnect()