def pyramide_erstellen(n):
    max_ziffern = len(str(n))
    max_breite = n * (max_ziffern + 1)
    for i in range(1, n + 1):
        # Leerzeichen vor den Zahlen einfügen
        leerzeichen = " " * ((max_breite - i * (max_ziffern + 1)) // 2)
        if i < 10:
            leerzeichen += " "
        print(leerzeichen, end="")
        # Zahlen einfügen
        ziffern = len(str(i))
        print((str(i) + " " * (max_ziffern - ziffern + 1)) * i)

# Nutzereingabe abfragen
try:
    zahl = int(input("Geben Sie eine ganze Zahl ein: "))
    pyramide_erstellen(zahl)
except ValueError:
    print("Bitte geben Sie eine gültige ganze Zahl ein.")
