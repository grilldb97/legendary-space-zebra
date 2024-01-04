from gui import MainWindow  # Import MainWindow-Klasse aus gui.py


class MainWecker:
    # Der Konstruktor der MainWecker-Klasse
    def __init__(self):

        self.window = MainWindow()  # Instanz MainWindow-Klasse erstellen; speichern in self.window

    # Definieren Sie die Methode run_wecker, die die show_window-Methode der MainWindow-Klasse aufruft
    def run_wecker(self):
        # Rufen Sie die Methode show_window der MainWindow-Klasse auf
        self.window.show_window()


# Überprüfen Sie, ob dieses Skript direkt ausgeführt wird (anstatt importiert zu werden)
if __name__ == "__main__":
    # Erstellen Sie eine Instanz der MainWecker-Klasse
    wecker = MainWecker()
    # Rufen Sie die Methode run_wecker der MainWecker-Klasse auf
    wecker.run_wecker()
    # Starten Sie die Tkinter event loop, um das Fenster anzuzeigen und auf Benutzerinteraktionen zu reagieren
    wecker.window.window.mainloop()
