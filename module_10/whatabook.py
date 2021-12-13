'''
Ryan Kite
CSD 310 
Module 10
Assignement WhatABook 
'''
import time
import sys
import mysql.connector
from mysql.connector import errorcode

# for displaying results as mysql tables
# pip install tabulate
from tabulate import tabulate

config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}

# Global variables
IS_RUNNING = True
USER_ID = 0
logo = "WhatABook 📖"
DB = None

# loader
import itertools, sys
spinner = itertools.cycle('◐◓◑◒')
def run_spinner():
    for i in range(16):
        sys.stdout.write(next(spinner))   # write the next character
        sys.stdout.flush()                # flush stdout buffer (actual character display)
        sys.stdout.write('\b')            # erase the last written char
        time.sleep(0.1)                   # pause between each frame

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

def close_db():
    global DB
    try: 
        DB.close()
        print("""\n\tclosing connection """)
    except AttributeError as e:
        print(f"DB was not used, skipping close action.")            

# display wishlist books for user_id
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

# display books not in users wishlist that they can add
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
        book_id = int(input(f"\n{logo}: Enter a book_id to add it to your Wishlist: >>> "))
        print(f"{logo}: Entered book_id [{book_id}]")
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
            is_valid = True
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
        
def remove_book():
    global DB
    # show wishlist
    show_wishlist()
    # get book_id to be removed
    book_id = int(input(f"\n{logo}: Enter book_id to be removed: >>> "))
    # delete (user_id, book_id) from wishlist
    DB = mysql.connector.connect(**config) 
    cursor = DB.cursor()
    cursor.execute(f"DELETE FROM wishlist WHERE user_id={USER_ID} AND book_id={book_id};")
    DB.commit()
    print(f"{logo}: Deleted book_id: [{book_id}] from Wishlist...❌")
    show_wishlist()

# display all books
def show_books():
    global DB
    DB = mysql.connector.connect(**config) 
    cursor = DB.cursor()
    cursor.execute("SELECT book_id, book_name, author, details FROM book;")
    results = cursor.fetchall()
    print(f"\n{logo}: Displaying Book Records \n")
    print(tabulate(results, headers=['book_id', 'book_name', 'author', 'details'], tablefmt='psql')) 

# display stores
def show_stores():
    global DB
    DB = mysql.connector.connect(**config) 
    cursor = DB.cursor()
    cursor.execute("SELECT store_id, address, location FROM store;")
    results = cursor.fetchall()
    print(f"\n{logo}: Store Locations \n")
    print(tabulate(results, headers=['store_id', 'address', 'location'], tablefmt='psql'))

# display wishlist menu
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

# display main menu
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

# Start program loop
while IS_RUNNING:
    if USER_ID != 0:
        show_wishlist_menu()
    else:
        show_menu()
        
