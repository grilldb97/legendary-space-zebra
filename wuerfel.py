import random
import time
n = int(input("Wie oft möchtest du würfeln? "))

treffer = 0
fehlwurf = 0

for i in range(n):
    augen = random.randint(1, 6)

    if augen == 6:
        print("Du hast die {0} gewürfelt. Herzlichen Glückwunsch".format(str(augen)))
        treffer = treffer+1
        time.sleep(2)
    else:
        print("Leider hast du die {0} gewürfelt. Probiere es erneut".format(str(augen)))
        fehlwurf = fehlwurf+1
        time.sleep(2)

time.sleep(2)
print("Du hast insgesamt " + str(treffer + fehlwurf) + " mal gewürfelt.")
time.sleep(3)
print("Davon waren " + str(treffer) + " Treffer und " + str(fehlwurf) + " Fehlwürfe.")
