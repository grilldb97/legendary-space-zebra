import sqlite3
import sys

verbindung = sqlite3.connect("datenbank1.db")
zeiger = verbindung.cursor()

match input("Was soll ausgeführt werden (1: Hinzufügen 2: Suchen)? "):
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
        zeiger.execute("SELECT * FROM personen")
        inhalt = zeiger.fetchall()

    case "2":
        nachname = input("Nachname: ")
        vorname = input("Vorname: ")
        geburtstag = input("Geburtstag: ")

        # Platzhalter bei leerer Eingabe
        if not nachname:
            nachname = '%'
        else:
            nachname += '%'  # Erlaube Wildcards am Ende
        if not vorname:
            vorname = '%'
        else:
            vorname += '%'  # Erlaube Wildcards am Ende
        if not geburtstag:
            geburtstag = '%'
        else:
            geburtstag += '%'  # Erlaube Wildcards am Ende

        zeiger.execute("""
            SELECT * FROM personen WHERE 
            nachname LIKE ? AND 
            vorname LIKE ? AND 
            geburtstag LIKE ?
        """, (nachname, vorname, geburtstag))

        inhalt = zeiger.fetchall()

        # Ausgabe der Ergebnisse
        for x in inhalt:
            print(x)
    case _:
        print("Invalid Input")
        sys.exit(-1)



sql_anweisung = """
CREATE TABLE IF NOT EXISTS personen (
vorname VARCHAR(20),
nachname VARCHAR(20),
geburtstag DATE
);"""



for x in inhalt:
    print(x, "\n")

verbindung.commit()
verbindung.close()
