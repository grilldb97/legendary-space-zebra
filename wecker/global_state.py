from tkinter import *


class GlobalState:
    def __init__(self):
        self._state = {}

    def get_state(self, wecker_index):
        return self._state.get(wecker_index, {}).get('state')

    def set_state(self, wecker_index, state):
        if wecker_index not in self._state:
            self._state[wecker_index] = {}
        self._state[wecker_index]['state'] = state


# Erstellen Sie eine Instanz von GlobalState
global_state = GlobalState()
