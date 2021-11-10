""""
Ryan Kite
CSD 310
Module 5
"""
def __main__():
    is_get = True
    while is_get:
        from pymongo import MongoClient
        url = 'mongodb+srv://admin:admin@kite.jjgxi.mongodb.net/pytech?retryWrites=true&w=majority'
        client = MongoClient(url)
        db = client.pytech
        collection = db.students
        print("\n-- Pytech Collection List --")
        print(db.list_collection_names())
        is_get = input("\n\nEnd of program press any key to exit: ")
        if is_get != True:
            break

__main__()
