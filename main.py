# demo.py

import logging
from time import sleep
from Instruments.instruments import Instruments

logger = logging.getLogger(__name__)

# Instanziere die Klasse
instruments = Instruments()

try:
    # Dynamisch das Gerät laden und verwenden
    #fluke_device_class = instruments.get_device('Instruments.DMM.Fluke.DMM_8845A')
    #fluke_device = fluke_device_class(interface_type="GPIB", interface_info={'address': 1}, ID=1)

    #fluke_device.set_Beep(1)
    #fluke_device.set_Beep(0)

    #fluke_device.set_Local() #??

    # 
    powersupply_device_class = instruments.get_device('Instruments.PowerSupply.RS310P')
    powersupply_device = powersupply_device_class(interface_type="Serial", interface_info={'port': "COM18"})

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
    state = powersupply_device.getOutputStats()         # Liest die Ausgangsstatistiken
    tVolt = powersupply_device.getTargetVolts()         # Liest die Zielspannung
    limit = powersupply_device.getCurrentLimit()        # Liest den Strombegrenzungswert

    protectValue = powersupply_device.getProtectionValues()    # Liest die Schutzspannungen
    protectState = powersupply_device.getProtectionState()     # Liest den Schutzstatus

    buzzer= powersupply_device.getBuzzer()              # Liest den Summerzustand



    sleep(3)  

    # Überprüfe, ob bestimmte Kombinationen erlaubt sind
#    print(fluke_device.is_combination_allowed("Null", "DCV"))  # Sollte 'Yes' zurückgeben
#    print(fluke_device.is_combination_allowed("dB", "Freq"))   # Sollte 'No' zurückgeben
#    print(fluke_device.is_combination_allowed("Limit", "Cap")) # Sollte 'Yes' zurückgeben
#    print(fluke_device.is_combination_allowed("Average", "Cont")) # Sollte 'No' zurückgeben



    # Selbsttest durchführen
#    print("Self-Test Result:", fluke_device.self_test())

    # Spannung messen
#    meas = fluke_device.get_VolatgeDC()
#    print(meas)

    # Route abrufen
#    print(fluke_device.get_ROUTE())

    # Frequenz messen
#    print(fluke_device.get_Frquency(fluke_device.constants.MeasurementMode.MEDIUM))

    # Mathematische Funktionen ein- und ausschalten
#    fluke_device.set_MATH(True)
#    fluke_device.set_MATH(False)
except Exception as e:      # works on python 3.x
    logger.error('Error: %s', repr(e))

finally:
    # Gerät trennen
    #fluke_device.disconnect()
    powersupply_device.disconnect()