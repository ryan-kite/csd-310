'''
Ryan Kite
CSD 310 
Module 9 
Assignement 9.2
'''

import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "pysports_user",
    "password": "csd_310",
    "host": "127.0.0.1",
    "database": "pysports",
    "raise_on_warnings": True
}

try:
    """ try/catch block for handling potential MySQL database errors """ 

    db = mysql.connector.connect(**config) # connect to the pysports database 
    
    # output the connection status 
    print("\n  Database user [{}] connected to MySQL on host [{}] with database [{}]".format(config["user"], config["host"], config["database"]))

    # Cursor Example
    cursor = db.cursor()

    cursor.execute("SELECT player_id, first_name, last_name, team_name FROM player INNER JOIN team ON player.team_id = team.team_id;")
    results = cursor.fetchall()
    print("\n--- DISPLAYING PLAYER RECORDS --- \n")
    for item in results:
        print(f"PLAYER ID: {item[0]}")
        print(f"First name: {item[1]}")
        print(f"Last name: {item[2]}")
        print(f"Team name: {item[3]}\n")
    
    
    input("\n\tPress any key to abort program...")

except mysql.connector.Error as err:
    """ on error code """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    print("""\n\n\tclosing connection to MySQL """)
    db.close()