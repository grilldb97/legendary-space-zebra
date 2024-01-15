from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem, ThreeLineListItem
from kivymd.uix.screen import Screen
import sqlite3
import datetime

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


def insert_into_db(vorname, nachname, geburtstag):
    verbindung = sqlite3.connect("datenbank1.db")
    zeiger = verbindung.cursor()
    zeiger.execute("""
            INSERT INTO personen 
                   VALUES (?,?,?)
           """,
                   (vorname, nachname, geburtstag)
                   )
    verbindung.commit()


class MyApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        # Get today's date
        global birthday_message
        today = datetime.date.today()
        # Format it in the same way as your database entries
        formatted_today = today.strftime('%d.%m')
        current_year = today.year

        # Connect to the database
        verbindung = sqlite3.connect("datenbank1.db")
        zeiger = verbindung.cursor()

        # Execute a query to find any birthdays that match today's date
        zeiger.execute("""
                SELECT * FROM personen
            """)

        # Fetch all records
        birthdays = zeiger.fetchall()

        for birthday in birthdays:
            vorname, nachname, geburtstag = birthday
            geburtstag_date = datetime.datetime.strptime(geburtstag, '%d.%m.%Y')
            if geburtstag_date.strftime('%d.%m') == formatted_today:
                age = current_year - geburtstag_date.year
                birthday_message = f"{vorname} {nachname} hat heute Geburtstag und ist jetzt {age} Jahre alt."

        self.root.ids.birthday_list.add_widget(ThreeLineListItem(text=birthday_message))

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


if __name__ == '__main__':
    MyApp().run()
