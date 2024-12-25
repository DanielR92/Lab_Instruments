# demo.py

import logging
from time import sleep
from Instruments.instruments import Instruments

logger = logging.getLogger(__name__)

# Instanziere die Klasse
instruments = Instruments()
fluke_device_class = instruments.get_device('Instruments.DMM.Fluke.DMM_8845A')
powersupply_device_class = instruments.get_device('Instruments.PowerSupply.RS310P')

fluke_device = None
powersupply_device = None

def main():
    global fluke_device, powersupply_device
    try:
        fluke_device = fluke_device_class(interface_type="GPIB", interface_info={'address': 1}, ID=1)
        powersupply_device = powersupply_device_class(interface_type="Serial", interface_info={'port': "COM18"})

        #resistor = fluke_device.get_Resistor2W()

        #fluke_device.set_Beep(1)
        #fluke_device.set_Beep(0)

        #fluke_device.set_Local() #??


        # Selbsttest durchführen
    #    print("Self-Test Result:", fluke_device.self_test())

        # Route abrufen
    #    print(fluke_device.get_ROUTE())

        # Frequenz messen
    #    print(fluke_device.get_Frquency(fluke_device.constants.MeasurementMode.MEDIUM))

        # Mathematische Funktionen ein- und ausschalten
    #    fluke_device.set_MATH(True)
    #    fluke_device.set_MATH(False)
            
    except Exception as e:      # works on python 3.x
        logger.error('Error: %s', repr(e))


def SetVoltage(volt: float):
    try:
        uncer = powersupply_device.res_volt  # Auflösung des Gerätes

        # Spannung setzen
        powersupply_device.setConfig(volt=volt, current=0.1, OVP=15, OCP=0.5, OPP=12)
        meas = fluke_device.get_VolatgeDC() # read voltage from DMM

        while(meas < volt-uncer or meas > volt+uncer):
            ps_volt = powersupply_device.getTargetVolts()   # read voltage from power supply

            if(meas < volt-uncer):
                powersupply_device.setVoltage(ps_volt + uncer)
            else:
                powersupply_device.setVoltage(ps_volt - uncer)

            meas = fluke_device.get_VolatgeDC()
            print(meas)
            sleep(1)
    
    except Exception as e:      # works on python 3.x
        logger.error('Error: %s', repr(e))


if __name__ == "__main__":
    main()
    #SetVoltage(24.53)
    #sleep(5)
    print("End of program")