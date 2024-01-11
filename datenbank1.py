import sqlite3
import sys

verbindung = sqlite3.connect("datenbank1.db")
zeiger = verbindung.cursor()
print("Datenbank - Geburtstage")


def search():
    nachname_search = input("Nachname: ")
    vorname_search = input("Vorname: ")
    geburtstag_search = input("Geburtstag: ")

    # Platzhalter bei leerer Eingabe
    if not nachname_search:
        nachname_search = '%'
    else:
        nachname_search += '%'  # Erlaube Wildcards am Ende
    if not vorname_search:
        vorname_search = '%'
    else:
        vorname_search += '%'  # Erlaube Wildcards am Ende
    if not geburtstag_search:
        geburtstag_search = '%'
    else:
        geburtstag_search += '%'  # Erlaube Wildcards am Ende

    zeiger.execute("""
            SELECT * FROM personen WHERE 
            nachname LIKE ? AND 
            vorname LIKE ? AND 
            geburtstag LIKE ?
        """, (nachname_search, vorname_search, geburtstag_search))

    inhalt_search = zeiger.fetchall()
    for x in inhalt_search:
        print(x)

    return nachname_search, vorname_search, geburtstag_search


def update_field(field_to_update, new_value, nachname_search, vorname_search, geburtstag_search):
    zeiger.execute(f"""
        UPDATE personen 
        SET {field_to_update} = ? 
        WHERE nachname LIKE ? AND vorname LIKE ? AND geburtstag LIKE ?
        """, (new_value, nachname_search, vorname_search, geburtstag_search))


sql_anweisung = """
CREATE TABLE IF NOT EXISTS personen (
vorname VARCHAR(20),
nachname VARCHAR(20),
geburtstag DATE
);"""

while True:
    user_input = input("Was soll ausgeführt werden?\n\n 1: Hinzufügen\n 2: Suchen\n 3: Bearbeiten\n 4: Löschen\n "
                       "5: Beenden")

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
                nachname == ? AND 
                vorname == ? AND 
                geburtstag == ?
            """, (nachname, vorname, geburtstag))
            inhalt = zeiger.fetchall()
            print(inhalt, "wurde der Datenbank hinzugefügt")
            verbindung.commit()
        case "2":  # Suchen
            search()
            verbindung.commit()
        case "3":  # Bearbeiten
            print("Suchen Sie die Person, wo Sie die Daten bearbeiten möchten")
            nachname_search, vorname_search, geburtstag_search = search()

            field_to_update = input(
                "Welches Feld möchtest du aktualisieren? (1: Vorname, 2: Nachname, 3: Geburtstag): ")
            new_value = input("Bitte gib den neuen Wert ein: ")

            match field_to_update:
                case "1":
                    update_field("vorname", new_value, nachname_search, vorname_search, geburtstag_search)
                case "2":
                    update_field("nachname", new_value, nachname_search, vorname_search, geburtstag_search)
                case "3":
                    update_field("geburtstag", new_value, nachname_search, vorname_search, geburtstag_search)
                case _:
                    print("Ungültige Eingabe. Bitte wähle entweder 1, 2 oder 3.")
            verbindung.commit()
        case "4":  # Löschen
            pass
            verbindung.commit()
        case "5":
            print("Programm beendet.")
            verbindung.close()
            break
        case _:
            print("Invalid Input")
            print("Ungültige Eingabe. Bitte wähle entweder 1, 2, 3, 4 oder 5.")
            sys.exit(-1)




