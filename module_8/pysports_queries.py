
'''
Ryan Kite
CSD 310 
Module 8 
Assignement 8.3
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
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    # Cursor Example
    cursor = db.cursor()

    cursor.execute("SELECT team_id, team_name, mascot FROM team")
    teams = cursor.fetchall()
    # print(teams)

    print("\n--- VIEW TEAM RECORDS --- ")
    for team in teams:
        print("\nTeam ID: {}".format(team[0]))
        print("Team Name: {}".format(team[1]))
        print("Mascot: {}".format(team[2]))
       
    cursor.execute("SELECT * FROM player")
    players = cursor.fetchall()
    # print(players)

    print("\n--- VIEW PLAYER RECORDS --- ")
    for player in players:
        print("\nPlayer ID: {}".format(player[0]))
        print("Firts Name: {}".format(player[1]))
        print("Last Name: {}".format(player[2]))   
        print("Team ID: {}".format(player[3]))
    
    
    input("\n\n\tPress any key to end program...")

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