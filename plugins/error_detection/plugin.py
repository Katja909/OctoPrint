import octoprint.plugin
from my_team_ki_model import FehlerErkennung  # Hier importierst du das KI-Modell

class MyPlugin(octoprint.plugin.OctoPrintPlugin):

    def initialize(self):
        # Initialisiere alle erforderlichen Ressourcen (z.B. das KI-Modell)
        self.fehlermodell = FehlerErkennung()
        self._logger.info("Plugin initialisiert.")

    def on_event(self, event, payload):
        if event == "PRINT_STARTED":
            self._logger.info("Druck gestartet. Fehlererkennung aktiviert.")
            self.start_fehlermonitoring()

    def start_fehlermonitoring(self):
        # Hier könntest du eine Echtzeitüberwachung einfügen, z.B. eine Methode, die kontinuierlich prüft
        # und Fehler in den Druckdaten erkennt.
        self.fehlermodell.pruefe_fehler_im_druck()

    def on_print_progress(self, storage, path, progress):
        # Rufe hier die Fehlererkennungslogik im Verlauf des Drucks auf
        if self.fehlermodell.erkennt_fehler(progress):
            self._logger.warning("Fehler erkannt im Druckprozess!")
            self.notify_user("Fehler erkannt!")

    def notify_user(self, message):
        # Sende Benachrichtigungen an den Benutzer
        self._plugin_manager.send_plugin_message(self._identifier, dict(type="error", message=message))

__plugin_name__ = "error_detection"
__plugin_implementation__ = MyPlugin()

#boolean methode die chekct ob wir der Druck gestartet haben
#boolean methode ob es ein Fehler gibt, wenn 1, dann break
#Methoden aus dem octorint repo importieren