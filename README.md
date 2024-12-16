# Lab Instrument automation Fluke 8845A Multimeter controller

Dies ist eine Python-basierte Bibliothek zur Steuerung des Fluke 8845A Multimeters. Sie ermöglicht die Kommunikation mit dem Gerät über verschiedene Schnittstellen (GPIB, seriell, TCPIP) und bietet eine Vielzahl von Funktionen zur Messung und Konfiguration des Multimeters.

## Funktionen

- **Schnittstellen**: Unterstützung für die Kommunikation mit dem Fluke 8845A über GPIB, serielle Schnittstellen oder TCP/IP.
- **Messungen**: Ermöglicht die Durchführung von Messungen in verschiedenen Modi (z.B. DC Spannung, AC Spannung, Widerstand, Strom, Frequenz).
- **Mathematische Funktionen**: Überprüft, ob bestimmte mathematische Funktionen (wie "Durchschnitt" oder "Null") mit den gewählten Messmodi kompatibel sind.
- **Gerätesteuerung**: Beinhaltet Funktionen zum Verbinden, Trennen und Zurücksetzen des Geräts.

## Installation

1. Klone das Repository:

    ```bash
    git clone https://github.com/deinbenutzername/fluke-8845a-multimeter.git
    ```

2. Installiere die benötigten Python-Pakete:

    ```bash
    pip install pyvisa
    ```

## Nutzung

### 1. Initialisierung des Geräts

Das Gerät kann mit einer der folgenden Schnittstellen verbunden werden: GPIB, Serial, TCPIP. Beispielsweise:

```python
from Instruments.DMM.Fluke.DMM_8845A import Device

# Beispiel für die Verbindung über GPIB
interface_info = {'address': 1}  # GPIB-Adresse
fluke_device = Device(interface_type="GPIB", interface_info=interface_info, ID=1)
