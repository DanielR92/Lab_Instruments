# demo.py

import logging
from time import sleep
from Instruments.instruments import Instruments


def main():
    logger = logging.getLogger(__name__)

    # Instanziere die Klasse
    instruments = Instruments()

    # Dynamisch das Gerät laden und verwenden
    fluke_device_class = instruments.get_device('Instruments.DMM.Fluke.DMM_8845A')
    fluke_device = None;

    try:
        fluke_device = fluke_device_class(interface_type="GPIB", interface_info={'address': 1}, ID=1)

        fluke_device.Error()
        resistor =fluke_device.get_Resistor2W()

        #fluke_device.set_Beep(1)
        #fluke_device.set_Beep(0)

        #fluke_device.set_Local() #??

        #powersupply_device_class = instruments.get_device('Instruments.PowerSupply.RS310P')
        #powersupply_device = powersupply_device_class(interface_type="Serial", interface_info={'port': "COM18"})

        #powersupply_device.setLConfig(volt=10, current=0.1, OVP=15, OCP=0.5, OPP=12)


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
    
        fluke_device.disconnect()
        
    except Exception as e:      # works on python 3.x
        logger.error('Error: %s', repr(e))

    finally:
        # Gerät trennen
        #powersupply_device.disconnect()

if __name__ == "__main__":
    main()
    print("End of program")