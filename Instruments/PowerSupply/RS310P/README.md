# RS310P Power Supply Control

Dieses Projekt bietet einen Treiber zur Steuerung und Verwaltung des RS310P Netzgeräts. Es enthält Klassen und Methoden zur Interaktion mit dem Netzgerät.

## Funktionen

- **Geräteverwaltung**: Dynamisches Laden und Verwenden des RS310P Netzgeräts.
- **Konfigurationen**: Methoden zur Konfiguration des Netzgeräts (z.B. Einstellen von Spannung, Strom, Überstromschutz).
- **Fehlerbehandlung**: Abrufen und Verarbeiten von Fehlermeldungen vom Netzgerät.

## Installation

1. Klone das Repository:
    ```sh
    git clone https://github.com/dein-benutzername/rs310p-power-supply-control.git
    ```
2. Wechsle in das Projektverzeichnis:
    ```sh
    cd rs310p-power-supply-control
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
    powersupply_device_class = instruments.get_device('Instruments.PowerSupply.RS310P')
    powersupply_device = powersupply_device_class(interface_type="Serial", interface_info={'port': "COM18"})

    # Konfiguration des Netzgeräts
    powersupply_device.setLConfig(volt=10, current=0.1, OVP=15, OCP=0.5, OPP=12)

    # Buzzer ein- und ausschalten
    powersupply_device.setBuzzer(True)
    powersupply_device.setBuzzer(False)

finally:
    # Gerät trennen
    powersupply_device.disconnect()