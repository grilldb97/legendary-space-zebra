from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.screen import Screen
import sqlite3
import datetime

verbindung = sqlite3.connect("datenbank1.db")
zeiger = verbindung.cursor()
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
            ScrollView:
                MDList:
                    id: result_list    
            MDRaisedButton:
                text: 'Hinzufügen'
                on_release: app.add_record()
                pos_hint: {'center_x': 0.5}
            MDRaisedButton:
                text: 'Suchen'
                on_release: app.search()
                size_hint: 0.10, 0.025
                pos_hint: {'top': 0.5 + self.size_hint[1]/2}
            MDRaisedButton:
                text: 'Bearbeiten'
                on_release: app.update_info()
                size_hint: 0.10, 0.025
                pos_hint: {'top': 0.5 + self.size_hint[1]/2}
            MDRaisedButton:
                text: 'Löschen'
                on_release: app.delete_info()
                pos_hint: {'center_x': 0.5}
            MDRaisedButton:
                text: 'Zurück'
                on_release: app.root.current = 'main'
                pos_hint: {'center_x': 0.5}
'''
vorname = ""
nachname = ""
geburtstag = ""


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vorname = ""
        self.nachname = ""
        self.geburtstag = ""
        self.verbindung = sqlite3.connect("datenbank1.db")
        self.zeiger = self.verbindung.cursor()

    def build(self):
        return Builder.load_string(KV)

    def input_fields(self):
        self.vorname = self.root.ids.vorname_input.text
        self.nachname = self.root.ids.nachname_input.text
        self.geburtstag = self.root.ids.geburtstag_input.text
        return vorname, nachname, geburtstag

    def on_start(self):
        # Get today's date
        today = datetime.date.today()
        # Format it in the same way as your database entries
        formatted_today = today.strftime('%d.%m')
        current_year = today.year

        # Execute a query to find any birthdays that match today's date
        zeiger.execute("""
                SELECT * FROM personen
            """)

        # Fetch all records
        birthdays = zeiger.fetchall()
        birthday_message = ''
        for birthday in birthdays:
            self.vorname, self.nachname, self.geburtstag = birthday
            if self.geburtstag:
                geburtstag_date = datetime.datetime.strptime(self.geburtstag, '%d.%m.%Y')
                if geburtstag_date.strftime('%d.%m') == formatted_today:
                    age = current_year - geburtstag_date.year
                    birthday_message = (f"{self.vorname} {self.nachname} "
                                        f"hat heute Geburtstag und ist jetzt {age} Jahre alt.")

        self.root.ids.result_list.add_widget(ThreeLineListItem(text=birthday_message))
        verbindung.commit()

    def add_record(self):
        zeiger.execute("""
                    INSERT INTO personen 
                           VALUES (?,?,?)
                   """,
                       (self.vorname, self.nachname, self.geburtstag)
                       )
        zeiger.execute("""
                SELECT * FROM personen WHERE 
                vorname == ? AND 
                nachname == ? AND 
                geburtstag == ?
            """, (self.vorname, self.nachname, self.geburtstag))
        inhalt = zeiger.fetchall()
        print(inhalt, "wurde der Datenbank hinzugefügt")
        verbindung.commit()
        print(f'Vorname: {self.vorname}, Nachname: {self.nachname}, Geburtstag: {self.geburtstag}')


    def search(self):
        # Platzhalter bei leerer Eingabe
        if not self.vorname:
            self.vorname = '%'
        else:
            self.vorname += '%'  # Erlaube Wildcards am Ende
        if not self.nachname:
            self.nachname = '%'
        else:
            self.nachname += '%'  # Erlaube Wildcards am Ende
        if not self.geburtstag:
            self.geburtstag = '%'
        else:
            self.geburtstag += '%'  # Erlaube Wildcards am Ende

        zeiger.execute("""
                SELECT * FROM personen WHERE 
                vorname LIKE ? AND 
                nachname LIKE ? AND 
                geburtstag LIKE ?
            """, (self.vorname, self.nachname, self.geburtstag))

        inhalt_search = zeiger.fetchall()
        results = '\n'.join([f"{i+1}. {x}" for i, x in enumerate(inhalt_search)])

        # Erstellen Sie ein neues Label mit den Suchergebnissen als Text
        results_label = MDLabel(text=results)

        # Fügen Sie das Label zu Ihrem Layout hinzu
        self.root.ids.result_list.add_widget(results_label)

        return inhalt_search, self.vorname, self.nachname, self.geburtstag

    def update(self):
        global vorname, nachname, geburtstag
        zeiger.execute(f"""
        UPDATE personen 
        SET {field_to_update} = ? 
        WHERE vorname LIKE ? AND nachname LIKE ? AND geburtstag LIKE ?
        """, (new_value, vorname, nachname, geburtstag))
        print("Datensatz wurde aktualisiert.")
        print(f"ALT: Vorname: {vorname_search}, Nachname: {nachname_search}, Geburtstag: {geburtstag_search}")
        print(f"UPDATED: Vorname: {new_value}, Nachname: {nachname_search}, Geburtstag: {geburtstag_search}")
        verbindung.commit()

    def delete_info(self):
        # Hier können Sie Ihre Datenbankoperationen durchführen
        # Zum Beispiel:
        # self.delete_in_db(vorname, nachname, geburtstag)
        pass


if __name__ == '__main__':
    MyApp().run()
