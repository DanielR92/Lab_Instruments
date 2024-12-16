from enum import Enum

# Andere Werte oder Konstanten
DEFAULT_TIMEOUT = 5000  # Zeitlimit in Millisekunden
MODEL_NAME = "Fluke 8845A"

math_function_matrix = {
    "Null":   {"DCV": "Yes", "ACV": "Yes", "DCI": "Yes", "ACI": "Yes", "2W": "Yes", "4W": "Yes",
               "Freq": "Yes", "Period": "Yes", "Cont": "No", "Diode": "No", "Temp": "Yes", "Cap": "Yes"},
    "Average": {"DCV": "Yes", "ACV": "Yes", "DCI": "Yes", "ACI": "Yes", "2W": "Yes", "4W": "Yes",
                "Freq": "Yes", "Period": "Yes", "Cont": "No", "Diode": "No", "Temp": "Yes", "Cap": "Yes"},
    "dB":     {"DCV": "No", "ACV": "Yes", "DCI": "No", "ACI": "No", "2W": "No", "4W": "No",
               "Freq": "No", "Period": "No", "Cont": "No", "Diode": "No", "Temp": "No", "Cap": "No"},
    "dBm":    {"DCV": "No", "ACV": "Yes", "DCI": "No", "ACI": "No", "2W": "No", "4W": "No",
               "Freq": "No", "Period": "No", "Cont": "No", "Diode": "No", "Temp": "No", "Cap": "No"},
    "Limit":  {"DCV": "Yes", "ACV": "Yes", "DCI": "Yes", "ACI": "Yes", "2W": "Yes", "4W": "Yes",
               "Freq": "Yes", "Period": "Yes", "Cont": "No", "Diode": "No", "Temp": "Yes", "Cap": "Yes"}
}

class MeasurementMode(Enum):
    CAPACITANCE = "CAP"

    VOLTAGE_DC_RATIO = "VOLT:DC:RAT"
    VOLTAGE_DC = "VOLT:DC"
    VOLTAGE_AC = "VOLT:AC"

    CURRENT_DC = "CURR:DC"
    CURRENT_AC = "CURR:AC"

    TWO_WIRE_RESISTANCE = "RES"
    FOUR_WIRE_RESISTANCE = "FRES"

    FREQUENCY = "FRE"
    PERIOD  = "PER"

    TWO_WIRE_TEMPERATURE = "TEMP:RTD"
    FOUR_WIRE_TEMPERATURE = "TEMP:FRTD"

    DIODE = "DIOD"
    CONTINUITY = "CONT"

# a number between the upper and lower limits of the function.
#class Range(Enum):
    MIN = "MIN"     # Lowest range of the function
    MAX = "MAX"     # Highest range of the function
    AUTO = "DEF"    # Autorange

#class Low_Current(Enum):
    ON = 1     # Sets diode current to 0.1 mA
    OFF = 0    # Sets diode current to 1 mA

#class Low_Voltage(Enum):
#    ON = 1     # Sets diode voltage to 5 volts
#    OFF = 0    # Sets diode voltage to 10 volts
 
# Set aperture time for frequency function
#class Aperture(Enum):
    FAST = 0.01     # Lowest range of the function
    MEDIUM = 0.1     # Highest range of the function
    SLOW = 1    # Autorange

# Current
#class Current(Enum):
#    ON = 1     # Sets diode current to 0.1 mA
#    OFF = 0     # Sets diode current to 1 mA

#class ONOFF(Enum):
#    ON = 1
#    OFF = 0

# Definiere die Matrix als Dictionary
