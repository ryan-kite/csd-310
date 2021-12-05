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
    print("\n Database user [{}] connected to MySQL on host [{}] with database [{}]".format(config["user"], config["host"], config["database"]))

    # Cursor Example
    cursor = db.cursor()

    # insert a new record into the player table for Team Gandalf which is team_id = 1
    cursor.execute("INSERT INTO player (first_name, last_name, team_id) VALUES('Smeagol', 'Shire Folk', 1)")
    
    # display records
    cursor.execute("SELECT player_id, first_name, last_name, team_name FROM player INNER JOIN team ON player.team_id = team.team_id;")
    results = cursor.fetchall()
    print("\n--- DISPLAYING PLAYER RECORDS AFTER INSERT --- \n")
    for item in results:
        print(f"PLAYER ID: {item[0]}")
        print(f"First name: {item[1]}")
        print(f"Last name: {item[2]}")
        print(f"Team name: {item[3]}\n")

    # update the newly inserted record by changing the players team to Team Sauron which is team_id = 2    
    cursor.execute("UPDATE player SET team_id=2 WHERE first_name='Smeagol' ")
    
    # display records
    cursor.execute("SELECT player_id, first_name, last_name, team_name FROM player INNER JOIN team ON player.team_id = team.team_id;")
    results = cursor.fetchall()
    print("\n--- DISPLAYING PLAYER RECORDS AFTER UPDATE --- \n")
    for item in results:
        print(f"PLAYER ID: {item[0]}")
        print(f"First name: {item[1]}")
        print(f"Last name: {item[2]}")
        print(f"Team name: {item[3]}\n")

    # delete the new record
    cursor.execute("DELETE FROM player WHERE first_name='Smeagol' ")
    
    # display records
    cursor.execute("SELECT player_id, first_name, last_name, team_name FROM player INNER JOIN team ON player.team_id = team.team_id;")
    results = cursor.fetchall()
    print("\n--- DISPLAYING PLAYER RECORDS AFTER DELETE --- \n")
    for item in results:
        print(f"PLAYER ID: {item[0]}")
        print(f"First name: {item[1]}")
        print(f"Last name: {item[2]}")
        print(f"Team name: {item[3]}\n")

    db.commit()
    
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