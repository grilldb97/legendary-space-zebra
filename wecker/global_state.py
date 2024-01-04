from tkinter import *


class GlobalState:
    def __init__(self):
        self._state = {}


    def get_state(self):
        return self._state.get(DISABLED)

    def set_state(self, state):
        self._state = state


# Erstellen Sie eine Instanz von GlobalState
global_state = GlobalState()