from ui import Window
from alarms import Alarm
import ui

# Erstellen Sie die StringVar-Objekte hier, nachdem das Fenster erstellt wurde
global button_labels

# Erstellen Sie eine leere Liste von Tabs am Anfang Ihres Programms
tabs = []

window = Window()
window.create_window()


if __name__ == "__main__":
    # Starten Sie den Hauptfenster-Thread
    Window.mainloop()
