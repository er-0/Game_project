Flying game! The file pilot_game_database.txt includes the instructions to edit the already existing flight_game database.

Edit db.py to include your MariaDB username and password.



###db.py 

```
import mysql.connector

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='database',
         user='root',
         password='password',
         autocommit=True
         )
```