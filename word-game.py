# funktiota
import random
def random_letters():
    letters = "ABCDEFGHIJKLMNOPRSTUVYÄÖ"
    return random.sample(letters, 8)

finnish = open("every-finnish-word.txt", encoding="utf-8")
finnish_words = [word.strip() for word in finnish]
finnish.close()

def is_it_finnish(word):
    return word.lower() in finnish_words

def valid_letters():

def word_points()

# pelin aloitus
total_points = 0
goal_points = 100
letters = random_letters()

print("Olet melkein perillä. Jäljellä on vielä onnistunut lasku. Laskeutuaksesi turvallisesti pelaa tämä peli läpi.")
print("Sanapelissä sinulle arvotaan kahdeksan kirjainta, joista muodostat suomekielisiä sanoja. Sanan tule olla vähintään kaksi kirjainta pitkä. Saat käyttää samaa kirjainta monta kertaa. ")

#whilelooppi pelaamiselle
while total_points < target_points:


# lopputulos
if goal_points >= target_points:
    print(f"Hienoa työtä! Olet onnistuneesti laskeutunut ja suorittanut lentosi. Koko-naispistemääräsi on {total_points}")
else:
    print("Laskeutuminen meni huonosti.  Matkustajat kokivat laskeutumisen vaa-rallisena ja epämukavana sekä vaativat korvauksia. Matkatavarat vahin-goittuivat ja yhtiö joutui maksamaan korvausmaksuja. Menetit lentolupasi etkä voi lentää.")
