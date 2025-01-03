# Lab Instrument Automation Controller

Dieses Projekt ist eine Python-basierte Bibliothek zur Steuerung von Laborinstrumenten wie dem Fluke 8845A Multimeter und dem RS310P Netzteil. Es ermöglicht die Kommunikation mit diesen Geräten über verschiedene Schnittstellen (GPIB, Seriell, TCPIP) und bietet eine Vielzahl von Funktionen für Messungen und Konfigurationen.

> [!WARNING]  
> This repo is currently in heavy development.

## Funktionen

- **Schnittstellen**: Unterstützung für die Kommunikation mit verschiedenen Messgeräten (z.B. Fluke 8845A) über GPIB, serielle Schnittstellen oder TCP/IP.
- **Messungen**: Ermöglicht Messungen in verschiedenen Modi (z.B. DC-Spannung, AC-Spannung, Widerstand, Strom, Frequenz).
- **Gerätesteuerung**: Beinhaltet Funktionen zum Verbinden, Trennen und Zurücksetzen des Geräts.

## Schnittstellenunterstützung

| Schnittstelle | Unterstützung |
|---------------|----------------|
| GPIB          | ✅ Unterstützt |
| Seriell       | ✅ Unterstützt |
| TCPIP         | ❌ Noch nicht unterstützt |

## ⚠️ Hinweis

Bitte beachten Sie, dass dieses Projekt noch Fehler enthalten kann und nicht vollumfänglich integriert ist. Wir arbeiten jedoch kontinuierlich daran, die Funktionalität zu verbessern und Fehler zu beheben.

## Treiber-Fortschritt

### Digital Multimeter (DMM)

| Gerät         | Fortschritt          |
|---------------|----------------------|
| [Fluke 8845A](https://github.com/DanielR92/Lab_Instruments/tree/main/Instruments/DMM/Fluke/DMM_8845A)   | ✅ Grundfunktionen implementiert |


### Power Supply

| Gerät         | Fortschritt          |
|---------------|----------------------|
| [RS310P](https://github.com/DanielR92/Lab_Instruments/tree/main/Instruments/PowerSupply/RS310P)        | ✅ Grundfunktionen implementiert |

## Installation

1. Repository klonen:

    ```bash
    git clone https://github.com/your-username/lab-instrument-automation.git
    ```

2. Erforderliche Python-Pakete installieren:

    ```bash
    pip install pyvisa pymodbus
    ```

## Verwendung

### 1. Initialisierung des Geräts

Das Gerät kann über eine der folgenden Schnittstellen verbunden werden: GPIB, Seriell, TCPIP. Zum Beispiel:

```python
from Instruments.DMM.Fluke.DMM_8845A import Device

# Beispiel für die Verbindung über GPIB
interface_info = {'address': 1}  # GPIB-Adresse
fluke_device = Device(interface_type="GPIB", interface_info=interface_info, ID=1)

# Beispiel für die Verbindung zum RS310P Netzteil über Seriell
from Instruments.PowerSupply.RS310P import Device as PowerSupplyDevice
interface_info = {'port': "COM18"}  # Serieller Port
powersupply_device = PowerSupplyDevice(interface_type="Serial", interface_info=interface_info)
```

### 2. Messungen durchführen

```python
# DC-Spannung messen
voltage = fluke_device.get_VolatgeDC()
print(f"Gemessene DC-Spannung: {voltage}")

# Konfigurieren und Messen mit dem Netzteil
powersupply_device.setLConfig(volt=10, current=0.1, OVP=15, OCP=0.5, OPP=12)
current_limit = powersupply_device.getCurrentLimit()
print(f"Strombegrenzung: {current_limit}")
```

### 3. Gerätesteuerung

```python
# Gerät zurücksetzen
fluke_device.reset()

# Gerät trennen
fluke_device.disconnect()
powersupply_device.disconnect()
```

## Beitrag

Beiträge sind willkommen! Bitte zögere nicht, einen Pull Request einzureichen.





Streamline your IPTV experience by consolidating multiple M3U playlists into a single source with the blazingly fast 🔥 and lightweight M3U Stream Merger Proxy. This service acts as a modern HTTP proxy server, effortlessly merging and streaming content from various M3U sources.

Uses the channel title or `tvg-name` (as fallback) to merge multiple identical channels into one. This is not an xTeVe/Threadfin replacement but is often used with it.

> [!IMPORTANT]  
> Under construction

> > [!NOTE]
> Help are heavly welcome

> [!TIP]
>  =)
