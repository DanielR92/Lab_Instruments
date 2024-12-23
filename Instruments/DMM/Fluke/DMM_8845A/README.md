# Lab Instruments Control

Dieses teil des Projekts bietet ein Treiber zur Steuerung und Verwaltung von Labor Instrumenten. Es enthält Klassen und Methoden zur Interaktion mit verschiedenen Messgeräten und Stromversorgungen.

## Funktionen

- **Messungen und Konfigurationen**: Methoden zur Durchführung von Messungen (z.B. DC-Spannung) und zur Konfiguration der Geräte (z.B. Einstellen von Bereichen und Auflösungen).
- **Fehlerbehandlung**: Abrufen und Verarbeiten von Fehlermeldungen von den Geräten.
- **Kalibrierung**: Abrufen von Kalibrierungsdaten.

## Installation

1. Klone das Repository:
    ```sh
    git clone https://github.com/dein-benutzername/lab-instruments-control.git
    ```
2. Wechsle in das Projektverzeichnis:
    ```sh
    cd lab-instruments-control
    ```
3. Installiere die Abhängigkeiten:
    ```sh
    pip install -r requirements.txt
    ```

## Verwendung

### Beispielcode

Hier ist ein Beispiel, wie du die Klassen und Methoden in deinem Projekt verwenden kannst:

```python
from Instruments.instruments import Instruments

# Instanziere die Klasse
instruments = Instruments()

try:
    # Dynamisch das Gerät laden und verwenden
    fluke_device_class = instruments.get_device('Instruments.DMM.Fluke.DMM_8845A')
    fluke_device = fluke_device_class(interface_type="GPIB", interface_info={'address': 1}, ID=1)
    fluke_device.Error()    # show if error is existing

    # Spannung messen
    meas = fluke_device.get_VolatgeDC()
    print(meas)

    # Route abrufen (Front or Read)
    print(fluke_device.get_ROUTE())

    # Frequenz messen
    print(fluke_device.get_Frquency(fluke_device.constants.MeasurementMode.MEDIUM))

    # Mathematische Funktionen ein- und ausschalten
    fluke_device.set_MATH(True)
    fluke_device.set_MATH(False)

finally:
    # Gerät trennen
    fluke_device.disconnect()