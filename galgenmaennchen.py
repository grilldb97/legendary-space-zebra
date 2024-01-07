import random

words = ['tulpe', 'lilie', 'gänseblümchen', 'orchidee']
word = random.choice(words)

print("Galgenmännchen, Blumen\n")

guesses = ''
turns = 10

while turns > 0:
    failed = 0
    for char in word:
        if char in guesses:
            print(char, end="")
        else:
            print("_", end="")
            failed += 1
    if failed == 0:
        print("\nDu hast gewonnen!")
        break
    guess = input("\n\nBuchstaben eingeben:")
    guesses += guess
    if guess not in word:
        turns -= 1
        print("Falsch")
        print("Du hast noch", + turns, 'weitere Versuche')
        if turns == 0:
            print("Du hast verloren")
