from db import yhteys

print("Olet ilmassa matkalla määränpäähäsi. Hätätilanne! Polttoaine on vähissä! Voit saada lisää polttoainetta ratkaisemalla tämän pelin. Jos epäonnistut, joudut tekemään hätälaskun.")

kokonaispisteet = (peli 1 + peli 2)
taso = 2


def get_count_game():
    sql = ""
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    return result

get_count_game()

# vähimmäispisteet laskupelistä = 55

pisteet = (peli 2)


if pisteet >=55:
    print(f"Ilmatankkaus onnistui! Voit jatkaa lentoasi. Tämän pelin pistemääräsi on {pisteet}. Kokonaistuloksesi on "{kokonaispisteet}")
    input("Haluatko jatkaa pelaamista?(Kyllä/Poistu)")
    if Kyllä:
        print("")
    else:
    print(f"Kokonaispisteesi on {kokonaispisteet}")
    break

else:
    print("Epäonnistuit ja jouduit tekemään hätälaskun. Sait {pisteet} pistettä.")
    input("Haluatko yrittää uudelleen? (Kyllä/Poistu)")