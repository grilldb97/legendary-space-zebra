from tkinter import Spinbox


class Spinboxes:
    def __init__(self):
        self.spinboxes = {}

    def create_spinboxes(self, parent, wecker_index):
        spinbox_stunden = Spinbox(parent, from_=0, to=23, width=5)
        spinbox_minuten = Spinbox(parent, from_=0, to=59, width=5)

        if wecker_index not in self.spinboxes:
            self.spinboxes[wecker_index] = {}

        self.spinboxes[wecker_index]['stunden'] = spinbox_stunden
        self.spinboxes[wecker_index]['minuten'] = spinbox_minuten

        return spinbox_stunden, spinbox_minuten

    def disable_spinboxes(self, wecker_index):
        self.spinboxes[wecker_index]['stunden'].config(state='disabled')
        self.spinboxes[wecker_index]['minuten'].config(state='disabled')

    def get_spinbox_values(self, wecker_index):
        stunden = self.spinboxes[wecker_index]['stunden'].get()
        minuten = self.spinboxes[wecker_index]['minuten'].get()
        return stunden, minuten
