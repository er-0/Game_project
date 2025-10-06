import random
def random_letters():
    letters = "ABCDEFGHIJKLMNOPRSTUVYÄÖ"
    return random.sample(letters, 8)



finnish = open("every-finnish-word.txt", encoding="utf-8")
finnish_words = [word.strip() for word in finnish]
finnish.close()

def is_it_finnish(word):
    return word.lower() in finnish_words

#testi
while True:
    word = input("anna sana: ")
    if not word:
        break
    if is_it_finnish(word):
        print("Oikein.")
    else:
        print("Sanaa ei löytynyt.")