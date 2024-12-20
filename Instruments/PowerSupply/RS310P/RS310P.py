import importlib
import logging
import os

from pymodbus.client.serial import ModbusSerialClient

class Device:
    """Repsonsible for providing an interface to the ETommens eTM-xxxxP Series PSU.
       Several Mfg's use this supply, Hanmatek HM305P, Rockseed RS305P,
       Hanmatek HM310P, RockSeed RS310P, Rockseed RS605P.

       Ref https://sigrok.org/wiki/ETommens_eTM-xxxxP_Series#Protocol

       This class supports

       Setting

       - Output on/off state
       - Output Voltage
       - Current limit
       - Over voltage protection
       - Over current protection
       - Over power protection
       - Setting the buzzer on/off state

       Getting

       - The output on/off state
       - The target output voltage
       - The actual output voltage (drops to 0 if output is off)
       - The output current
       - The output power
       - The current limit value
       - The over voltage protection value
       - The over current protection value
       - The over power protection value

       """
    
    logger = logging.getLogger(__name__)
    
    MIN_VOLTAGE                     = 0
    MAX_VOLTAGE                     = 32.0
    MAX_OVER_VOLTAGE                = 33.0  #This is the max value that can be set on the PSU
    MAX_CURRENT                     = 10.0  #10A max, some models have a 5A max current.
    MAX_OVER_CURRENT                = 10.5  #This is the max value that can be set on the PSU
    MAX_OVER_POWER                  = 310.0 #This is the max value that can be set on the PSU
    #RW REG
    OUTPUT_STATE_REG_ADDR           = 0x0001
    #R REGS
    PROTECTION_STATE_REG_ADDR       = 0x0002
    MODEL_ID_REG_ADDR               = 0x0004
    OUTPUT_VOLTAGE_REG_ADDR         = 0x0010
    OUTPUT_CURRENT_REG_ADDR         = 0x0011
    OUTPUT_PWR_HI_REG_ADDR          = 0x0012 #Top 16 bits of output power reg
    OUTPUT_PWR_LO_REG_ADDR          = 0x0013 #Bottom 16 bits of output power reg
    #R/WR REGS
    VOLTAGE_TARGET_REG_ADDR     = 0x0030
    CURRENT_LIMIT_REG_ADDR      = 0x0031
    OVER_VOLTAGE_PROT_REG_ADDR  = 0x0020
    OVER_CURRENT_PROT_REG_ADDR  = 0x0021
    OVER_PWR_PROT_HI_REG_ADDR   = 0x0022    #Top 16 bits of over power protection
    OVER_PWR_PROT_LOW_REG_ADDR  = 0x0023    #Bottom 16 bits of over power protection
    BUZZER_REG_ADDR             = 0x8804    # 1 = enable (beep on key press), 0 = disable

    def __init__(self, interface_type, interface_info, ID):
        self.ID = ID

        # Verwende das interface_info Dictionary für den Aufbau der Schnittstelle
        if interface_type == "Serial":
            from Instruments.communication.serial import SerialInterface
            interface_info.update({'baudrate': 9600,'protocol': 'rtu'})
            self.interface = SerialInterface(**interface_info)
        else:
            raise ValueError(f"Unbekannter Schnittstellentyp: {interface_type}")
            return;
        self._connect()

    def _connect(self):
        """Verbindet mit dem Gerät."""
        self.interface.connect()
        print(f"Verbinde mit Gerät über {self.interface} mit ID {self.ID}.")

    def disconnect(self):
        """Trennt die Verbindung zum Gerät."""
        self.interface.disconnect()
        print("Verbindung zum Gerät getrennt.")

    def set_voltage(self, voltage):
        try:
            self.logger.info(f"Setze Spannung auf {voltage} V.")
            self.interface.write_register(Device.VOLTAGE_TARGET_REG_ADDR, int(voltage * 100), unit=self.ID)
        except Exception as e:
            self.logger.error(f"Fehler beim Setzen der Spannung: {e}")
            raise

    def get_actual_voltage(self):
        raw_value = self.interface.read_register(self.OUTPUT_VOLTAGE_REG_ADDR)
        return raw_value[0] / 100.0  # Annahme: Antwort in 0.01 V Schritten
