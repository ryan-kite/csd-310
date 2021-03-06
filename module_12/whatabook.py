'''

Ryan Kite
CSD 310 
Module 10, 11, 12 (combined work and progress)
Capstone Assignement WhatABook 

Code attribution:
The run_spinner() method was inspired from a post on StacK Overflow
https://stackoverflow.com/questions/4995733/how-to-create-a-spinning-command-line-cursor

The SQL connection code is similar as used in previous assignments.

Requirement:
There is 1 dependency that needs to be installed for the project, called tabulate. (See below or in the readme.txt)
It will display query result in the same way MySQL does in the shell. 

IMPORTS:
'''
import time             # Used for the spinner.
import sys              # Used for the spinner.
import itertools        # Used for the spinner.
import mysql.connector  # Allows us to do CRUD actions with MySQL.
from mysql.connector import errorcode   # If connector throws error.

# WARNING WARNING WARNING WARNING
# PLEASE INSTALL THIS LIBRARY
# its for displaying results as a MySQL tables in the python shell
# from your command prompt run: 
# pip install tabulate
from tabulate import tabulate


# This is the MySQL connector payload.
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}

# Global variables used in the app. 
IS_RUNNING = True
USER_ID = 0
logo = "WhatABook 📖"
DB = None

# Shows a spinner the in the python shell to simulate 
# a loading effect between screens and actions.
spinner = itertools.cycle('◐◓◑◒') # what the spinner cycles through. 
def run_spinner():
    for i in range(16):
        sys.stdout.write(next(spinner))   # write the next character
        sys.stdout.flush()                # flush stdout buffer (actual character display)
        sys.stdout.write('\b')            # erase the last written char
        time.sleep(0.1)                   # pause between each frame

# Handles generating a DB connection object and returns a cursor used to performs DB actions
# It's assigned it to a global which was easier that having to pass it around between methods
# for this small app I thinks thats OK. 
def get_db():
    global DB
    try:
        """ try/catch block for handling potential MySQL database errors """ 
        DB = mysql.connector.connect(**config) 
        # output the connection status 
        # print("\n Database user [{}] connected to MySQL on host [{}] with database [{}]".format(config["user"], config["host"], config["database"]))
        # Cursor Example
        cursor = DB.cursor()
        return cursor
    except mysql.connector.Error as err:
        """ on error code """
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("The supplied username or password are invalid")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("The specified database does not exist")
        else:
            print(err)
    finally:
        print("""\n\n\tclosing connection """)
        DB.close()

# Handles closing the DB when we are finished using it.
def close_db():
    global DB
    try: 
        DB.close()
        print("""\n\tclosing connection """)
    except AttributeError as e:
        print(f"DB was not used, skipping close action.")            

# Handles displaying wishlist books for the user_id
# This method utilized 4 JOINS
def show_wishlist():
    global DB
    DB = mysql.connector.connect(**config) 
    cursor = DB.cursor()
    cursor.execute(f'''SELECT wishlist.user_id, user.first_name, user.last_name, wishlist.book_id, book.book_name, store.store_id, store.location
    FROM wishlist
    INNER JOIN user
    ON user.user_id = wishlist.user_id  
    INNER JOIN book
    ON wishlist.book_id = book.book_id
    INNER JOIN store
    ON book.store_id = store.store_id
    WHERE user.user_id = {USER_ID}''')
    results = cursor.fetchall()
    print(f"\n{logo}: Displaying Wishlist Books \n")
    print(tabulate(results, headers=['user_id', 'first_name', 'last_name', 'book_id', 'book_name', 'store_id', 'location'], tablefmt='psql'))

# Handles displaying books not in users wishlist that they can add
# Also performs some deeper validation against the selected book
# vs the book_list, with exception handling. With a go back option.
def show_available_books():
    global DB
    DB = mysql.connector.connect(**config) 
    cursor = DB.cursor()
    cursor.execute(f'''SELECT book_id, book_name, author, details 
        FROM book WHERE book_id 
        NOT IN (SELECT book_id from wishlist where user_id = {USER_ID});''')
    results = cursor.fetchall()
    print(f"\n{logo}: Available Books \n")
    print(tabulate(results, headers=['book_id', 'book_name', 'author', 'details'], tablefmt='psql'))
    # get book_id from user
    try: 
        print(f"{logo}: Enter book_id to add to Wishlist: ")
        print(f"{logo}: Enter [ x ] to go back: ")
        book_id = input(f"\n{logo}: >>> ")
        print(f"{logo}: Entered [{book_id}]")
        if book_id.lower().strip() == 'x':
            show_wishlist_menu()
        elif book_id:
            book_id = int(book_id)
            cursor.execute(f'''SELECT book_id
                FROM book WHERE book_id 
                NOT IN (SELECT book_id from wishlist where user_id = {USER_ID});''')
            book_ids = cursor.fetchall()  
            # print("book_ids", book_ids) 
            # print("book_ids", type(book_ids))
            book_id_list = []
            for item in book_ids:
                book_id_list.append(item[0])
                # print(book_id_list)
            # validate book selection against book_ids
            if book_id in book_id_list:
                # print(f"book_id: {book_id} == {book_id_list}") 
                print(f"{logo}: valid book entry...✅")
                cursor = DB.cursor()
                cursor.execute(f'''INSERT INTO 
                        wishlist (user_id, book_id)
                        VALUES ({USER_ID}, {book_id});''')
                DB.commit()
                print(f"{logo}: Added book to Wishlist")
                show_wishlist()
            else:
                raise Exception("book_id was not found.")    
    except Exception as e:
        print(f"{logo}: Whoa let's try that again: [ {e} ]...👀")
        show_wishlist_menu()

# This was an bonus function added in because I needed it.
# Handles removing a books from wishlist, performs validation 
# and has expection handling. With a go back option.
def remove_book():
    # show wishlist
    show_wishlist()
    # get list of book_ids that can be deleted to validate against the selection
    DB = mysql.connector.connect(**config) 
    cursor = DB.cursor()
    cursor.execute(f'''SELECT book_id FROM wishlist WHERE user_id={USER_ID};''')
    book_ids = cursor.fetchall() 
    # print(book_ids)
    book_id_list = []
    for item in book_ids:
        book_id_list.append(item[0])
    # get book_id to be removed
    try:
        print(f"{logo}: Enter book_id to be removed: ")
        print(f"{logo}: Enter [ x ] to go back: ")
        book_id = input(f"\n{logo}: >>> ")
        print(f"{logo}: Entered [{book_id}]")
        if book_id.lower().strip() == 'x':  
            show_wishlist_menu()
        elif book_id:
            book_id = int(book_id)
            if book_id in book_id_list:
                DB = mysql.connector.connect(**config) 
                cursor = DB.cursor()
                cursor.execute(f"DELETE FROM wishlist WHERE user_id={USER_ID} AND book_id={book_id};")
                DB.commit()
                print(f"{logo}: Deleted book_id: [{book_id}] from Wishlist...❌")
                show_wishlist()
            else:
                raise Exception("book_id was not found.") 

    except Exception as e:
        print(f"{logo}: Whoa let's try that again: [ {e} ]...👀")
        show_wishlist_menu()

# Handles displaying all books.
def show_books():
    global DB
    DB = mysql.connector.connect(**config) 
    cursor = DB.cursor()
    cursor.execute("SELECT book_id, book_name, author, details FROM book;")
    results = cursor.fetchall()
    print(f"\n{logo}: Displaying Book Records \n")
    print(tabulate(results, headers=['book_id', 'book_name', 'author', 'details'], tablefmt='psql')) 

# Handles displaying store information.
def show_stores():
    global DB
    DB = mysql.connector.connect(**config) 
    cursor = DB.cursor()
    cursor.execute("SELECT store_id, address, location FROM store;")
    results = cursor.fetchall()
    print(f"\n{logo}: Store Locations \n")
    print(tabulate(results, headers=['store_id', 'address', 'location'], tablefmt='psql'))

# Handles displaying wishlist menu for active user + exception handling.
def show_wishlist_menu():
    global USER_ID
    print(f"\n{logo}: [Wishlist Menu]")
    print(f"{logo}: logged in as 👤 user_id: [ {USER_ID} ]")
    print(f"{logo}: Press [ 1 ] Wishlist")
    print(f"{logo}: Press [ 2 ] Add Book")
    print(f"{logo}: Press [ 3 ] Remove Book")
    print(f"{logo}: Press [ x ] Exit to Main menu")
    result = input(f"\n{logo}: Make a selection: >>> ")
    try:
        print(f"{logo}: You selected: [ {result} ]")
        run_spinner()
        if result == '1':
            show_wishlist()
        elif result == '2':
            show_available_books()
        elif result == '3':
            remove_book()     
        elif result.lower().strip() == 'x':
            USER_ID = 0 
        else:
            print(f"{logo}: Input not recognized: [ {result} ]...👀")
    except Exception as e:
        print(f"{logo}: Whoa let's try that again: [ {e} ]...👀")
        pass

# Handles displaying main public menu + exception handling.
def show_menu():
    print(f"\n{logo}: [Main Menu] ")
    print(f"{logo}: Press [ 1 ] View Books")
    print(f"{logo}: Press [ 2 ] View Store Locations")
    print(f"{logo}: Press [ 3 ] My Account")
    print(f"{logo}: Press [ x ] Exit")
    result = input(f"\n{logo}: Make a selection: >>> ")
    try: 
        print(f"{logo}: You selected: [ {result} ]") 
        run_spinner()
        if result == '1':
            show_books()
        elif result == '2':
            show_stores()
        elif result == '3':
            print(f"\n{logo}: Which User Account ID?")
            print(f"{logo}: Press [ 1 ] for Ryan ")
            print(f"{logo}: Press [ 2 ] for Gabriel ")
            print(f"{logo}: Press [ 3 ] for Aila ")
            try:
                result = int(input(f"\n{logo}: Enter Account ID: >>> ").strip())
                global USER_ID
                if result < 4:
                    USER_ID = result  
                    print(f"{logo}: Using Account: [ {USER_ID} ]")
                else:
                    print(f"\n{logo}: *** Invalid Account ID...👀")
            except Exception as e:
                print(f"{logo}: Whoa let's try that again: [ {e} ]...👀")
                show_menu()        
        elif result.lower().strip() == 'x':
            global IS_RUNNING 
            IS_RUNNING = False
            print(f"{logo}: See you next time 👋")
            close_db()
        else:
            print(f"{logo}: Input not recognized: [ {result} ]...👀")
    except Exception as e:
        print(f"{logo}: Whoa let's try that again: [ {e} ]...👀")
        pass

# Handles the program loop and will always return the appropriate menu 
# based on user_id state.
while IS_RUNNING:
    if USER_ID != 0:
        show_wishlist_menu()
    else:
        show_menu()
