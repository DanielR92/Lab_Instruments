# demo.py

import logging
from time import sleep
from Instruments.instruments import Instruments

logger = logging.getLogger(__name__)

# Instanziere die Klasse
instruments = Instruments()

try:
    # Dynamisch das Gerät laden und verwenden
    fluke_device_class = instruments.get_device('Instruments.DMM.Fluke.DMM_8845A')
    fluke_device = fluke_device_class(interface_type="GPIB", interface_info={'address': 1}, ID=1)

    #fluke_device.set_Beep(1)
    #fluke_device.set_Beep(0)

    #fluke_device.set_Local() #??


    # Überprüfe, ob bestimmte Kombinationen erlaubt sind
#    print(fluke_device.is_combination_allowed("Null", "DCV"))  # Sollte 'Yes' zurückgeben
#    print(fluke_device.is_combination_allowed("dB", "Freq"))   # Sollte 'No' zurückgeben
#    print(fluke_device.is_combination_allowed("Limit", "Cap")) # Sollte 'Yes' zurückgeben
#    print(fluke_device.is_combination_allowed("Average", "Cont")) # Sollte 'No' zurückgeben



    # Selbsttest durchführen
#    print("Self-Test Result:", fluke_device.self_test())

    # Spannung messen
    meas = fluke_device.get_VolatgeDC()
    print(meas)

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
    fluke_device.disconnect()