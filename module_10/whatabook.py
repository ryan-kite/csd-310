'''
Ryan Kite
CSD 310 
Module 10
Assignement WhatABook 
'''
import mysql.connector
from mysql.connector import errorcode

# for mysql tables
# pip install tabulate
from tabulate import tabulate

config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}

# program loop
IS_RUNNING = True
USER_ID = 0

def get_db():
    try:
        """ try/catch block for handling potential MySQL database errors """ 
        db = mysql.connector.connect(**config) # connect to the pysports database 
        # output the connection status 
        # print("\n Database user [{}] connected to MySQL on host [{}] with database [{}]".format(config["user"], config["host"], config["database"]))
        # Cursor Example
        cursor = db.cursor()
        return cursor
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

def show_wishlist():
    # display wishlist books for user_id
    db = mysql.connector.connect(**config) 
    cursor = db.cursor()
    cursor.execute(f'''SELECT wishlist.user_id, user.first_name, user.last_name, wishlist.book_id, book.book_name
    FROM wishlist
    INNER JOIN user
    ON user.user_id = wishlist.user_id  
    INNER JOIN book
    ON wishlist.book_id = book.book_id
    WHERE user.user_id = {USER_ID}''')
    
    results = cursor.fetchall()

    print("\n--- DISPLAYING WISHLIST BOOKS --- \n")
    print(tabulate(results, headers=['user_id', 'first_name', 'last_name', 'book_id', 'book_name'], tablefmt='psql'))

def show_available_books():
    # display books not in users wishlist that they can add
    db = mysql.connector.connect(**config) 
    cursor = db.cursor()
    cursor.execute(f'''SELECT book_id, book_name, author, details 
        FROM book WHERE book_id 
        NOT IN (SELECT book_id from wishlist where user_id = {USER_ID});''')
    
    results = cursor.fetchall()

    print("\n--- DISPLAYING AVAILABLE BOOKS --- \n")
    print(tabulate(results, headers=['book_id', 'book_name', 'author', 'details'], tablefmt='psql'))

    book_id = int(input("\nEnter a book_id to add it to your Wishlist:  "))
    print(f"Entered book_id [{book_id}]")
    cursor.execute(f'''SELECT book_id
        FROM book WHERE book_id 
        NOT IN (SELECT book_id from wishlist where user_id = {USER_ID});''')
    book_ids = cursor.fetchall()   
    print("book_ids", book_ids)
    valid_entry = None
    for item in book_ids:
        print(f"is book_id: [{item[0]}] == {book_id}") 
        if book_id == item[0]:
            valid_entry = True
            print("valid_entry: ", valid_entry)
            break
        else:
            valid_entry = False
            print("valid_entry: ", valid_entry)
    try:
        if valid_entry:
            cursor = db.cursor()
            cursor.execute(f'''INSERT INTO 
                    wishlist (user_id, book_id)
                    VALUES ({USER_ID}, {book_id});''')
            db.commit()
            print("ADDED book to Wishlist")
            show_wishlist()

        else:
            print("INVALID book_id")
    except Exception as e:
        print(f"Exception: {e}")
        show_wishlist_menu() 
        
def remove_book():
    # show wishlist
    show_wishlist()

    # get book_id to be removed
    book_id = int(input("\nEnter book_id to be removed:  "))

    # delete (user_id, book_id) from wishlist
    db = mysql.connector.connect(**config) 
    cursor = db.cursor()
    cursor.execute(f'''DELETE FROM wishlist WHERE user_id={USER_ID} AND book_id={book_id};''')
    db.commit()
    print(f"DELETED book_id: [{book_id}] from Wishlist...")
    # show wishlist
    show_wishlist()

def show_books():
    # display all books 
    db = mysql.connector.connect(**config) # connect to the pysports database 
    cursor = db.cursor()
    cursor.execute("SELECT book_id, book_name, details, author FROM book;")
    results = cursor.fetchall()
    print("\n--- DISPLAYING BOOK RECORDS --- \n")
    for item in results:
        print(f"Book ID: {item[0]}")
        print(f"Book name: {item[1]}")
        print(f"Detais: {item[2]}")
        print(f"Author: {item[3]}\n")

def show_stores():
    # display all books 
    db = mysql.connector.connect(**config) # connect to the pysports database 
    cursor = db.cursor()
    cursor.execute("SELECT store_id, locale FROM store;")
    results = cursor.fetchall()
    print("\n--- DISPLAYING STORE LOCATIONS --- \n")
    for item in results:
        print(f"Store ID: {item[0]}")
        print(f"Locale: {item[1]}")

def show_wishlist_menu():
    global USER_ID
    print("\nWhatABook: Wishlist Menu")
    print(f"For user_id: [ {USER_ID} ]")
    print("[ 1 ] Wishlist")
    print("[ 2 ] Add Book")
    print("[ 3 ] Remove Book")
    print("[ x ] Exit to Main")
    result = input("\nMake a selection:  ")
    print(f"You selected: [ {result} ]")

    if result == '1':
        show_wishlist()
    elif result == '2':
        show_available_books()
    elif result == '3':
        remove_book()     
    elif result.lower().strip() == 'x':
        USER_ID = 0 
    else:
        print("\n*** INVALID Selection")
        print("*** Please try again\n")          

def show_menu():
    print("\nWhatABook: Main Menu")
    print("[ 1 ] View Books")
    print("[ 2 ] View Store Locations")
    print("[ 3 ] My Account")
    print("[ x ] Exit")
    
    result = input("\nMake a selection:  ")
    print(f"You selected: [ {result} ]") 
    
    if result == '1':
        show_books()
    
    elif result == '2':
        show_stores()

    elif result == '3':
        print("\nWhich user account?")
        print("[ 1 ] Ryan ")
        print("[ 2 ] Gabriel ")
        print("[ 3 ] Aila ")
        try:
            result = int(input("\nEnter ID:  ").strip())
            global USER_ID
            if result < 4:
                USER_ID = result  
                print(f"Using Account: [ {USER_ID} ]")
            else:
                print("\n*** INVALID Account ID")
                print("*** Please try again\n")
        except Exception as e:
            print(f"INVALID entry: {e}")
            show_menu()        

    
    elif result.lower().strip() == 'x':
        global IS_RUNNING 
        IS_RUNNING = False
    else:
        print("\n*** INVALID Selection")
        print("*** Please try again\n")

while IS_RUNNING:
    if USER_ID != 0:
        show_wishlist_menu()
    else:
        show_menu()

