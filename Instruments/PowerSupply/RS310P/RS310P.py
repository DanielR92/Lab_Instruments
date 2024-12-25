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

    @property
    def res_volt(self):
        return 0.01  # Auflösung für Spannungsmessung

    @property
    def res_curr(self):
        return 0.01  # Auflösung für Strommessung

    @property
    def res_power(self):
        return 0.001  # Auflösung für Leistungsmessung

    def __init__(self, interface_type, interface_info, unit=1, slave=1):
        print("[Init:Start]-----------------------------")
        self._unit = unit
        self.slave= slave

        # Verwende das interface_info Dictionary für den Aufbau der Schnittstelle
        if interface_type == "Serial":
            from Instruments.communication.serial import SerialInterface
            interface_info.update({'baudrate': 9600, 'protocol': 'rtu'})
            self._client = SerialInterface(**interface_info)
        else:
            raise ValueError(f"Unbekannter Schnittstellentyp: {interface_type}")
        self._connect()
        self.Identification()
        print("[Init:Done]-----------------------------")

    def __del__(self):
        print("Delete Module 'RS310P' ... ", end=" ")
        self.disconnect()
        print(" ... done.")

    def Identification(self):
        ''' Retrieves the Meter’s identification. '''
        self._manufacturer  = "Rockseed"
        self._model         = "RS310P"
        self._serialnumber  = 0
        self._SWversion     = 0
        #self._SWDispVersion = teile[4]

    def _connect(self):
        """@brief connect to the PSU over the serial port."""
        self._client = ModbusSerialClient(method='rtu', port=self._client.port, baudrate=9600, stopbits=1, bytesize=8, timeout=1) 
        self._client.connect()

    def disconnect(self):
        """Trennt die Verbindung zum Gerät."""
        if (self.getOutput()):
            self.setOutput(0)   # Output is on, turn it off before disconnecting
        else:
            print("Device is already off.", end=" ")    # Device is off, no need to disconnect

        self._client.close()
        print("disconnected " + str(self._model), end=" ")

    def get_actual_voltage(self):
        raw_value = self._client.read_holding_registers(self.OUTPUT_VOLTAGE_REG_ADDR, slave=1)
        return raw_value.getRegister(0) / 100.0  # Annahme: Antwort in 0.01 V Schritten
    
    def setCurrentLimit(self, amps):
        """@brief Set the current limit value.
        @param amps The current in amps (a float value)."""
        if amps < 0.0 or amps > self.MAX_CURRENT:
            raise ValueError("{} is an invalid current value (valid range 0A - {}A)".format(amps, self.MAX_CURRENT))
        self._client.write_register(self.CURRENT_LIMIT_REG_ADDR , int(amps*1000.0), unit=self._unit, slave=self.slave)


    def setVoltage(self, voltage):
        """@brief Set the output voltage.
        @param voltage The voltage in volts (a float value)."""
        if voltage < self.MIN_VOLTAGE or voltage > self.MAX_VOLTAGE:
            raise ValueError("{} is an invalid voltage (valid range {}V - {}V)".format(voltage, self.MIN_VOLTAGE, self.MAX_VOLTAGE))
        self._client.write_register(self.VOLTAGE_TARGET_REG_ADDR , int(voltage*100.0), unit=self._unit, slave=self.slave)




    ### WRITE REGS ###
    def setConfig(self, volt, current, OVP, OCP, OPP, output=1):
        """@brief Set the PSU configuration.
        @param value The configuration value."""
        self.setVoltage(volt)
        self.setCurrentLimit(current)
        self.setOverVoltageP(OVP)
        self.setOverCurrentP(OCP)
        self.setOverPowerP(OPP)
        self.setOutput(output)

    def setOutput(self, on):
        """@brief Set The PSU output on/off.
        @param on If True the PSU output is on."""
        self._client.write_register(self.OUTPUT_STATE_REG_ADDR , on, unit=self._unit, slave=1)

    def setOverVoltageP(self, voltage):
        """@brief Set the over voltage protection value.
        @param voltage The voltage in volts (a float value)."""
        if voltage < self.MIN_VOLTAGE or voltage > self.MAX_OVER_VOLTAGE:
            raise ValueError("{} is an invalid voltage (valid range {}V - {}V)".format(voltage, self.MIN_VOLTAGE, self.MAX_VMAX_OVER_VOLTAGEOLTAGE))
        self._client.write_register(self.OVER_VOLTAGE_PROT_REG_ADDR , int(voltage*100.0), unit=self._unit, slave=self.slave)

    def setOverCurrentP(self, amps):
        """@brief Set the over current protection value.
        @param amps The current in amps (a float value)."""
        if amps < 0.0 or amps > self.MAX_OVER_CURRENT:
            raise ValueError("{} is an invalid voltage (valid range 0V - {}V)".format(amps, self.MAX_OVER_CURRENT))
        self._client.write_register(self.OVER_CURRENT_PROT_REG_ADDR , int(amps*1000.0), unit=self._unit, slave=self.slave)

    def setOverPowerP(self, watts):
        """@brief Set the over power protection value.
        @param watts The power in watts (a float value)."""
        if watts < 0.0 or watts > self.MAX_OVER_POWER:
            raise ValueError("{} is an invalid power (valid range 0W - {}W)".format(watts, self.MAX_OVER_POWER))
        wattValue = int((watts*1000))
        wattsL = wattValue&0x0000ffff
        wattsH = (wattValue&0xffff0000)>>16
        self._client.write_register(self.OVER_PWR_PROT_HI_REG_ADDR , wattsH, unit=self._unit, slave=self.slave)
        self._client.write_register(self.OVER_PWR_PROT_LOW_REG_ADDR , wattsL, unit=self._unit, slave=self.slave)

    def setBuzzer(self, on):
        """@brief Set the buzzer on/off.
        @param on If True the buzzer is set on, 0 = off."""
        self._client.write_register(self.BUZZER_REG_ADDR , on, unit=self._unit, slave=self.slave)




     ### READ REGS ###
    def getOutput(self):
        """@brief Get the state of the PSU output.
           @return 1 if the output is on, else 0."""
        rr = self._client.read_holding_registers(self.OUTPUT_STATE_REG_ADDR, 1, unit=self._unit, slave=self.slave)
        return bool(rr.getRegister(0))
    
    def getProtectionState(self):
        """@brief Get the state of the protections switch.
           @return 1 if protection mode is enabled, else 0."""
        rr = self._client.read_holding_registers(self.PROTECTION_STATE_REG_ADDR, 1, unit=self._unit, slave=self.slave)
        return rr.getRegister(0)

    def getModel(self):
        """@brief Get the model ID
           @return The model ID value"""
        rr = self._client.read_holding_registers(self.MODEL_ID_REG_ADDR, 1, unit=self._unit, slave=self.slave)
        return rr.getRegister(0)

    def getOutputStats(self):
        """@brief Read the output voltage, current and power of the PSU.
           @return A tuple containing
                   0: voltage
                   1: amps
                   2: watts"""
        rr = self._client.read_holding_registers(self.OUTPUT_VOLTAGE_REG_ADDR, 4, unit=self._unit, slave=self.slave)
        voltage = float(rr.getRegister(0))
        if voltage > 0:
            voltage=voltage/100.0
        amps = float(rr.getRegister(1))
        if amps > 0:
            amps=amps/1000.0
        wattsH = rr.getRegister(2)
        wattsL = rr.getRegister(3)
        watts = wattsH<<16|wattsL
        if watts > 0:
            watts=watts/1000.0
        return (voltage, amps, watts)

    def getTargetVolts(self):
        """@brief Read the target output voltage
           @return The output voltage set in volts."""
        rr = self._client.read_holding_registers(self.VOLTAGE_TARGET_REG_ADDR, 1, unit=self._unit, slave=self.slave)
        voltage = float(rr.getRegister(0))
        if voltage > 0:
            voltage=voltage/100.0
        return voltage

    def getCurrentLimit(self):
        """@brief Read the current limit in amps
           @return The current limit."""
        rr = self._client.read_holding_registers(self.CURRENT_LIMIT_REG_ADDR, 1, unit=self._unit, slave=self.slave)
        amps = float(rr.getRegister(0))
        if amps > 0:
            amps=amps/1000.0
        return amps

    def getProtectionValues(self):
        """@brief Read the over voltage, current and power protection values
           @return A tuple containing
                   0: over voltage protection value
                   1: over current protection value
                   2: over power protection value"""
        rr = self._client.read_holding_registers(self.OVER_VOLTAGE_PROT_REG_ADDR, 4, unit=self._unit, slave=self.slave)
        voltage = float(rr.getRegister(0))
        if voltage > 0:
            voltage=voltage/100.0
        amps = float(rr.getRegister(1))
        if amps > 0:
            amps=amps/1000.0
        wattsH = rr.getRegister(2)
        wattsL = rr.getRegister(3)
        watts = float(wattsH<<16|wattsL)
        if watts > 0:
            watts=watts/1000.0
        return (voltage, amps, watts)

    def getBuzzer(self):
        """@brief Get the state of the buzzer
           @return 1 if enabled, 0 if disabled."""
        rr = self._client.read_holding_registers(self.BUZZER_REG_ADDR, 1, unit=self._unit, slave=self.slave)
        return rr.getRegister(0)
    
    if __name__ == "__main__":
        print("This module is not intended to run standalone.")
        print("Please import it in your main program.")
        print("Exiting...")
        exit(1)