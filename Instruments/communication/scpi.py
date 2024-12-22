class scpi:
    def identification(self):
        """
        Liest die Identifikation des Geräts aus.
        """
        if self.device:
            return self.query("*IDN?")
        else:
            return "Keine aktive Verbindung zum Gerät."
    
    def reset(self):
        """
        Setzt das Gerät zurück.
        """
        if self.device:
            self.write("*RST")
            return "Gerät wurde zurückgesetzt."
        else:
            return "Keine aktive Verbindung zum Gerät."

    def self_test(self):
        """
        Führt einen Selbsttest durch und gibt das Ergebnis zurück.
        """
        if self.device:
            return self.query("*TST?")
        else:
            return "Keine aktive Verbindung zum Gerät."
    
    def clear_status(self):
        """
        Löscht den Status des Geräts.
        """
        if self.device:
            self.write("*CLS")
            return "Gerätestatus wurde gelöscht."
        else:
            return "Keine aktive Verbindung zum Gerät."
    
    def set_measurement_mode(self, mode):
        """
        Setzt den Messmodus des Geräts.
        :param mode: Der Messmodus (z.B. VOLT:DC, CURR:AC, etc.).
        """
        if self.device:
            self.write(f"CONF:{mode}")
            return f"Messmodus auf {mode} gesetzt."
        else:
            return "Keine aktive Verbindung zum Gerät."

    def read_measurement(self):
        """
        Liest den aktuellen Messwert.
        """
        if self.device:
            return self.query("READ?")
        else:
            return "Keine aktive Verbindung zum Gerät."
    
    def fetch_measurement(self):
        """
        Holt den zuletzt gemessenen Wert.
        """
        if self.device:
            return self.query("FETCH?")
        else:
            return "Keine aktive Verbindung zum Gerät."
    
    def configure_voltage_dc(self, range="AUTO", resolution="DEF"):
        """
        Konfiguriert eine DC-Spannungsmessung.
        :param range: Messbereich (z.B. 10, 100, "AUTO").
        :param resolution: Auflösung (z.B. "MAX", "MIN", "DEF").
        """
        if self.device:
            self.write(f"CONF:VOLT:DC {range}, {resolution}")
            return f"DC-Spannungsmessung mit Bereich {range} und Auflösung {resolution} konfiguriert."
        else:
            return "Keine aktive Verbindung zum Gerät."
    
    def configure_resistance(self, mode="2W", range="AUTO", resolution="DEF"):
        """
        Konfiguriert eine Widerstandsmessung.
        :param mode: Messmodus ("2W" oder "4W").
        :param range: Messbereich (z.B. 10, 100, "AUTO").
        :param resolution: Auflösung (z.B. "MAX", "MIN", "DEF").
        """
        if self.device:
            if mode == "2W":
                self.write(f"CONF:RES {range}, {resolution}")
            elif mode == "4W":
                self.write(f"CONF:FRES {range}, {resolution}")
            else:
                return f"Ungültiger Modus: {mode}"
            return f"Widerstandsmessung ({mode}) mit Bereich {range} und Auflösung {resolution} konfiguriert."
        else:
            return "Keine aktive Verbindung zum Gerät."
    
    def set_math_function(self, function):
        """
        Aktiviert eine mathematische Funktion.
        :param function: Die mathematische Funktion (z.B. "NULL", "AVERAGE", "DB").
        """
        if self.device:
            self.write(f"CALC:FUNC {function}")
            self.write("CALC:STAT ON")
            return f"Mathematische Funktion {function} aktiviert."
        else:
            return "Keine aktive Verbindung zum Gerät."
    
    def disable_math_function(self):
        """
        Deaktiviert die mathematischen Funktionen.
        """
        if self.device:
            self.write("CALC:STAT OFF")
            return "Mathematische Funktionen deaktiviert."
        else:
            return "Keine aktive Verbindung zum Gerät."
    
    def set_trigger(self, source="IMM"):
        """
        Konfiguriert die Triggerquelle.
        :param source: Triggerquelle (z.B. "IMM", "EXT", "BUS").
        """
        if self.device:
            self.write(f"TRIG:SOUR {source}")
            return f"Triggerquelle auf {source} gesetzt."
        else:
            return "Keine aktive Verbindung zum Gerät."
    
    def initiate_measurement(self):
        """
        Startet eine manuelle Messung.
        """
        if self.device:
            self.write("INIT")
            return "Manuelle Messung gestartet."
        else:
            return "Keine aktive Verbindung zum Gerät."
    
    def abort_measurement(self):
        """
        Stoppt eine laufende Messung.
        """
        if self.device:
            self.write("ABOR")
            return "Messung abgebrochen."
        else:
            return "Keine aktive Verbindung zum Gerät."
