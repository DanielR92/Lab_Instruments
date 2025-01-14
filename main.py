# demo.py

import logging
from time import sleep
from Instruments.instruments import Instruments

logger = logging.getLogger(__name__)

# Instanziere die Klasse
instruments = Instruments()
VS481C_device_class = instruments.get_device('Instruments.Switch.Aten.VS481C')


def main():
    try:
        hdmi_switch = VS481C_device_class(interface_type="Serial", interface_info={'port': "COM1"})
        
        hdmi_switch.set_priotity(2)

        hdmi_switch.set_input(0)
        hdmi_switch.set_input(1)
        hdmi_switch.set_input(2)
        hdmi_switch.set_input(3)
        hdmi_switch.set_input(4)

        hdmi_switch.set_POD(True)
        hdmi_switch.set_POD(False)

    except Exception as e:      # works on python 3.x
        logger.error('Error: %s', repr(e))


if __name__ == "__main__":
    main()
    print("End of program")