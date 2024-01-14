from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
import sqlite3

# KivyMD Layout
KV = '''
ScreenManager:
    Screen:
        name: 'main'
        BoxLayout:
            orientation: 'vertical'
            MDLabel:
                text: 'Geburtstage'
                halign: 'center'
            ScrollView:
                MDList:
                    id: birthday_list
            MDRaisedButton:
                text: 'Datenbank'
                on_release: app.root.current = 'database'
                pos_hint: {'center_x': 0.5}
    Screen:
        name: 'database'
        BoxLayout:
            orientation: 'vertical'
            MDTextField:
                id: vorname_input
                hint_text: 'Vorname'
            MDTextField:
                id: nachname_input
                hint_text: 'Nachname'
            MDTextField:
                id: geburtstag_input
                hint_text: 'Geburtstag'
            MDRaisedButton:
                text: 'Hinzufügen'
                on_release: app.submit_info()
                pos_hint: {'center_x': 0.5}
            MDRaisedButton:
                text: 'Suchen'
                on_release: app.search_info()
                pos_hint: {'center_x': 0.5}
            MDRaisedButton:
                text: 'Bearbeiten'
                on_release: app.update_info()
                pos_hint: {'center_x': 0.5}
            MDRaisedButton:
                text: 'Löschen'
                on_release: app.delete_info()
                pos_hint: {'center_x': 0.5}
            MDRaisedButton:
                text: 'Zurück'
                on_release: app.root.current = 'main'
                pos_hint: {'center_x': 0.5}
'''

class MyApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        # Hier können Sie Ihre Datenbankoperationen durchführen, um die aktuellen Geburtstage zu erhalten
        # Zum Beispiel:
        # birthdays = self.get_birthdays_from_db()
        # for birthday in birthdays:
        #     self.root.ids.birthday_list.add_widget(MDLabel(text=birthday))

        pass

    def submit_info(self):
        vorname = self.root.ids.vorname_input.text
        nachname = self.root.ids.nachname_input.text
        geburtstag = self.root.ids.geburtstag_input.text
        # Hier können Sie Ihre Datenbankoperationen durchführen
        # Zum Beispiel:
        # self.insert_into_db(vorname, nachname, geburtstag)
        print(f'Vorname: {vorname}, Nachname: {nachname}, Geburtstag: {geburtstag}')

    def search_info(self):
        # Hier können Sie Ihre Datenbankoperationen durchführen
        # Zum Beispiel:
        # self.search_in_db(vorname, nachname, geburtstag)
        pass

    def update_info(self):
        # Hier können Sie Ihre Datenbankoperationen durchführen
        # Zum Beispiel:
        # self.update_in_db(vorname, nachname, geburtstag)
        pass

    def delete_info(self):
        # Hier können Sie Ihre Datenbankoperationen durchführen
        # Zum Beispiel:
        # self.delete_in_db(vorname, nachname, geburtstag)
        pass

    def insert_into_db(self, vorname, nachname, geburtstag):
        verbindung = sqlite3.connect("datenbank1.db")
        zeiger = verbindung.cursor()
        zeiger.execute("""
                INSERT INTO personen 
                       VALUES (?,?,?)
               """,
                       (vorname, nachname, geburtstag)
                       )
        verbindung.commit()

if __name__ == '__main__':
    MyApp().run()
