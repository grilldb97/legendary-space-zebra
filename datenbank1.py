import sqlite3
import sys

verbindung = sqlite3.connect("datenbank1.db")
zeiger = verbindung.cursor()
print("Datenbank - Geburtstage")


def search():
    vorname_search = input("Vorname: ")
    nachname_search = input("Nachname: ")
    geburtstag_search = input("Geburtstag: ")

    # Platzhalter bei leerer Eingabe
    if not vorname_search:
        vorname_search = '%'
    else:
        vorname_search += '%'  # Erlaube Wildcards am Ende
    if not nachname_search:
        nachname_search = '%'
    else:
        nachname_search += '%'  # Erlaube Wildcards am Ende
    if not geburtstag_search:
        geburtstag_search = '%'
    else:
        geburtstag_search += '%'  # Erlaube Wildcards am Ende

    zeiger.execute("""
            SELECT * FROM personen WHERE 
            vorname LIKE ? AND 
            nachname LIKE ? AND 
            geburtstag LIKE ?
        """, (vorname_search, nachname_search, geburtstag_search))

    inhalt_search = zeiger.fetchall()
    for i, x in enumerate(inhalt_search):
        print(f"{i+1}. {x}")

    return inhalt_search, vorname_search, nachname_search, geburtstag_search


def update_field(field_to_update, new_value, vorname_search, nachname_search, geburtstag_search):
    zeiger.execute(f"""
        UPDATE personen 
        SET {field_to_update} = ? 
        WHERE vorname LIKE ? AND nachname LIKE ? AND geburtstag LIKE ?
        """, (new_value, vorname_search, nachname_search, geburtstag_search))
    print("Datensatz wurde aktualisiert.")
    print(f"ALT: Vorname: {vorname_search}, Nachname: {nachname_search}, Geburtstag: {geburtstag_search}")
    print(f"UPDATED: Vorname: {new_value}, Nachname: {nachname_search}, Geburtstag: {geburtstag_search}")
    verbindung.commit()


sql_anweisung = """
CREATE TABLE IF NOT EXISTS personen (
vorname VARCHAR(20),
nachname VARCHAR(20),
geburtstag DATE
);"""


def delete(vorname_search, nachname_search, geburtstag_search):
    zeiger.execute("""
    DELETE FROM personen
    WHERE vorname=? AND nachname=? AND geburtstag=?
    """, (vorname_search, nachname_search, geburtstag_search))
    print(f"Vorname: {vorname_search}, Nachname: {nachname_search}, Geburtstag: {geburtstag_search} wurde gelöscht")

while True:
    user_input = input("Was soll ausgeführt werden?\n 1: Hinzufügen\n 2: Suchen\n 3: Bearbeiten\n 4: Löschen\n "
                       "5: Beenden\n")

    match user_input:
        case "1":
            nachname = input("Nachname: ")
            vorname = input("Vorname: ")
            geburtstag = input("Geburtstag: ")

            zeiger.execute("""
                    INSERT INTO personen 
                           VALUES (?,?,?)
                   """,
                           (vorname, nachname, geburtstag)
                           )
            zeiger.execute("""
                SELECT * FROM personen WHERE 
                vorname == ? AND 
                nachname == ? AND 
                geburtstag == ?
            """, (vorname, nachname, geburtstag))
            inhalt = zeiger.fetchall()
            print(inhalt, "wurde der Datenbank hinzugefügt")
            verbindung.commit()
        case "2":  # Suchen
            search()
            verbindung.commit()
        case "3":  # Bearbeiten
            print("Suchen Sie die Person, wo Sie die Daten bearbeiten möchten")
            inhalt_search, vorname_search, nachname_search, geburtstag_search = search()

            if len(inhalt_search) > 1:
                auswahl = input("Bitte wählen Sie die Nummer der Person aus, die Sie bearbeiten möchten: ")
                auswahl = int(auswahl) - 1  # Korrigiere den Index
                vorname_search, nachname_search, geburtstag_search = inhalt_search[auswahl]

            while True:
                field_to_update = input("Welches Feld möchtest du aktualisieren? (1: Vorname, 2: Nachname, 3: Geburtstag): ")
                if field_to_update in ["1", "2", "3"]:
                    break
                else:
                    print("Ungültige Eingabe. Bitte wähle entweder 1, 2 oder 3.")
            new_value = input("Bitte gib den neuen Wert ein: ")

            match field_to_update:
                case "1":
                    update_field("vorname", new_value, vorname_search, nachname_search, geburtstag_search)
                case "2":
                    update_field("nachname", new_value, vorname_search, nachname_search, geburtstag_search)
                case "3":
                    update_field("geburtstag", new_value, vorname_search, nachname_search, geburtstag_search)
                case _:
                    print("Ungültige Eingabe. Bitte wähle entweder 1, 2 oder 3.")
            verbindung.commit()
        case "4":  # Löschen
            print("Suchen Sie die Person, wo Sie die Daten löschen möchten")
            inhalt_search, vorname_search, nachname_search, geburtstag_search = search()

            if len(inhalt_search) > 1:
                auswahl = input("Bitte wählen Sie die Nummer der Person aus, die Sie bearbeiten möchten: ")
                auswahl = int(auswahl) - 1  # Korrigiere den Index
                vorname_search, nachname_search, geburtstag_search = inhalt_search[auswahl]
            delete(vorname_search, nachname_search, geburtstag_search)
            verbindung.commit()
        case "5":
            print("Programm beendet.")
            verbindung.close()
            break
        case _:
            print("Invalid Input")
            print("Ungültige Eingabe. Bitte wähle entweder 1, 2, 3, 4 oder 5.")
            sys.exit(-1)




