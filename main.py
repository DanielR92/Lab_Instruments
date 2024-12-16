# demo.py
from Instruments.instruments import Instruments

# Instanziere die Klasse
instruments = Instruments()

# Dynamisch das Gerät laden und verwenden
fluke_device_class = instruments.get_device('Instruments.DMM.Fluke.DMM_8845A')
fluke_device = fluke_device_class(interface_type="GPIB", interface_info={'address': 1}, ID=1)


print(fluke_device.is_combination_allowed("Null", "DCV"))  # Sollte 'Yes' zurückgeben
print(fluke_device.is_combination_allowed("dB", "Freq"))   # Sollte 'No' zurückgeben
print(fluke_device.is_combination_allowed("Limit", "Cap")) # Sollte 'Yes' zurückgeben
print(fluke_device.is_combination_allowed("Average", "Cont")) # Sollte 'No' zurückgeben



# Measure Voltage
meas = fluke_device.get_VolatgeDC()
print(meas)


# Sense Measure
#??print(fluke_device.sense_measure("MEAS?"))

#print(fluke_device.get_CurrentDC_mA())
#print(fluke_device.get_CurrentDC_10A())

print(fluke_device.get_ROUTE())

print(fluke_device.get_Frquency(fluke_device.constants.MeasurementMode.MEDIUM))

fluke_device.set_MATH(True)
fluke_device.set_MATH(False)

#print(fluke_device.measure())
fluke_device.disconnect()