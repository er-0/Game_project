import mysql.connector

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='school_project',
    user='elizavetazhogol',
    password='HelloElizaveta!_2025',
    autocommit=True
    )


# Function to register users ---------------------------------------------------------------------------

def loggin():

    name = input('Give me your name: ')

    sql = f"SELECT COUNT(*) FROM players WHERE user_name = '{name}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    count = kursori.fetchone()[0]  

    while count != 0:
         
        print("This name already exists in the darabase")
        print("Try amother name")

        name = input('Give me your name: ')

        sql = f"SELECT COUNT(*) FROM players WHERE user_name = '{name}';"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        count = kursori.fetchone()[0]

    sql = f"SELECT ident FROM game_airports ORDER BY RAND() LIMIT 1;"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    ident = kursori.fetchone()[0]  

    sql = f"SELECT COUNT(*) FROM players WHERE starting_airport = '{ident}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    count_airport = kursori.fetchone()[0] 

    while count_airport != 0:

        sql = f"SELECT ident FROM game_airports ORDER BY RAND() LIMIT 1;"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        ident = kursori.fetchone()[0]  

        sql = f"SELECT COUNT(*) FROM players WHERE starting_airport = '{ident}';"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        count_airport = kursori.fetchone()[0]

    sql = f"INSERT INTO players (user_name, starting_airport) VALUES ('{name}','{ident}');"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    yhteys.commit()

    return 

loggin()

# -------------------------------------------------------------------------------------------------------

# Function to fetch all information from the databse on the user ----------------------------------------

def player_information(name):

    sql = f"SELECT a.name, a.continent, a.municipality, a.country_name FROM game_airports AS a INNER JOIN players AS p ON p.starting_airport = a.ident where p.user_name = '{name}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    users_information = kursori.fetchall()
    
    return users_information

name = input('Give me your name: ')

users_information = player_information(name)

for user_information in users_information:
        airport_name, airport_continent, airport_municipality, airport_country = user_information

print(airport_name)
print(airport_continent)
print(airport_municipality)
print(airport_country)

# -----------------------------------------------------------------------------------------------------

# print("Hello player! Have you played before:" \
# "If yes select 1" \
# "If no select 2")

# yes_no = int(input('Give your answer: '))

# if yes_no == 1:
#     print("Yes")
# elif yes_no == 2:
#     print("You need to register as a new pilot")
#     print("Select a unique name for yourself")

#     loggin()
