# Hauptprogramm - Wecker
import ui

def main():
    # Erstelle das Fenster
    window = ui.MyWindow()

    # Starte den Hauptloop
    window.mainloop()

def set_alarm(index, hours, minutes):
    # Speichere die Alarmzeit
    ui.tabs[index].alarm_time = (hours, minutes)


def snooze():
    # Verschiebe den Alarm um 10 Minuten
    ui.alarm_time = (ui.alarm_time[0], ui.alarm_time[1] + 10)


def stop_alarm():
    # Setze die Alarmzeit auf None
    ui.alarm_time = None


def show_help():
    print("Hilfetext")


if __name__ == "__main__":
    main()
