# Hauptprogramm - Wecker
import ui

def main():
    # Erstelle das Fenster
    ui.MyWindow()


class UIInterface:
    def set_alarm_time(self, time):
        pass

def update_alarm_time(ui, hours, minutes):
    ui.alarm_time = (hours, minutes)

def set_alarm(ui, index, hours, minutes):
    update_alarm_time(ui, hours, minutes)

def snooze(ui):
    hours, minutes = ui.alarm_time
    update_alarm_time(ui, hours, minutes + 10)


def show_help():
    print("Hilfetext")


if __name__ == "__main__":
    main()
