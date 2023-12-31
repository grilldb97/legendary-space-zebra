from tkinter import *
class HelpWindow:
    def help_content(self):
        help_window = Toplevel()
        help_window.title("Hilfe")
        help_window.geometry("300x200")
        Label(help_window, text="Hier sind die Anweisungen...").pack()