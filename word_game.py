from db import yhteys
import random

# tiedostosta listaan
finnish = open("finnish-words.txt", encoding="utf-8")
finnish_words = []
for line in finnish:
    word = line.strip()
    finnish_words.append(word.lower())
finnish.close()

# funktiot
def random_letters():
    letters = "abcdefghijklmnoprstuvyöä"
    sample_letters = random.sample(letters, 10)
    return " ".join(sample_letters)

def is_finnish(word):
    return word in finnish_words

def valid_letters(word, letters):
    for character in word:
        if character not in letters:
            return False
    return True

def word_points(word):
    length = len(word)
    if 2 <= length <= 3:
        return 4
    elif 4 <= length <= 5:
        return 10
    elif length >= 6:
        return 15
    else:
        return 0

def word_game():
    # pelin aloitus
    total_points = 0
    goal_points = 100
    letters = random_letters()

    print("Olet melkein perillä. Jäljellä on vielä onnistunut lasku. Laskeutuaksesi turvallisesti pelaa tämä peli läpi.\n")
    print("PELIN SÄÄNNÖT\n")
    print("Sanapelissä sinulle arvotaan 10 kirjainta, joista muodostat suomenkielisiä sanoja. \nSanan tule olla vähintään kaksi kirjainta pitkä. Saat käyttää samaa kirjainta monta kertaa. ")
    print("Jos et pysty muodostamaan sanaa arvotuista kirjaimista, paina enter ja sinulle arvotaan uudet kirjaimet. \nVoit lopettaa pelin kirjoittamalla vastauskenttään 'exit'.\n")
    print(f"Arvotut kirjaimet: {letters.upper()}")

    # pääohjelma

    while total_points < goal_points:
        word = input("\nArvaa sana: ").lower()

        if word == "exit":
            print("Peli lopetettu.")
            break

        elif word == "":
            letters = random_letters()
            print("Valitsit uudet kirjaimet:")
            print(letters.upper())
            continue

        letters_ok = valid_letters(word, letters)
        finnish_ok = is_finnish(word)

        if not letters_ok:
            print("Sana sisältää kirjaimia, joita ei ole annettu.")
            points = 0

        elif not finnish_ok:
            print("Sana ei ole sanakirjassa.")
            points = 0

        else:
            points = word_points(word)
            total_points += points
            print(f"Sana '{word}' on oikein! Sait {points} pistettä.")
            letters = random_letters()
            print("Seuraavat 10 kirjainta:")
            print(letters.upper())

    # lopputulos
    if total_points >= goal_points:
        print(f"Hienoa työtä! Olet onnistuneesti laskeutunut ja suorittanut lentosi. Kokonaispistemääräsi on {total_points}.")
    else:
        print("Laskeutuminen meni huonosti. Matkustajat kokivat laskeutumisen vaarallisena ja epämukavana.")
        print("Matkatavarat vahingoittuivat ja yhtiö joutui maksamaan korvausmaksuja.")
        print(f"Lopullinen pistemääräsi on {total_points}. Menetit lentolupasi etkä voi lentää.")
        print("Tarvitset lisäkoulutuksen. Kun olet valmis yrittämään uudelleen, palaa takaisin.")
        print(f"Lopullinen piste pistemääräsi on {total_points}. Lensit traagiset [kilometrit] kilometriä reitillä [aloituskenttä] – [kohdekenttä].")

    return total_points

if __name__ == "__main__":
    word_game()