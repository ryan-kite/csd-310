""" 
Ryan Kite
CSD 310
Nov 18, 2021
Module 6
Assignment 6.2
Description: 
Updating Documents
"""

# imports 
from pymongo import MongoClient
# connection uri
url = "mongodb+srv://admin:admin@kite.jjgxi.mongodb.net/pytech?retryWrites=true&w=majority"
# create client
client = MongoClient(url)
# get the pytech database
db = client.pytech

# querying 
# get students collection 
students = db.students

# # find all students in collection 
student_list = students.find()

# # loop over collection 
print("\n*** Displaying all documents using .find() query")
for doc in student_list:
    print(f'\n  Student ID: {doc["student_id"]} \n  First Name: {doc["first_name"]}  \n  Last Name:  {doc["last_name"]}')

# Call the update_one method by student_id 1007 and update the last name to something different than the originally saved name.
print("\n*** Calling .update() on student_id 1007\n")
res = students.update_one({"student_id": "1007"}, {"$set": {"last_name": "FooFoo"}})
# print("result: ", dir(res))
print("Acknowledged: ", res.acknowledged)
print("Matched_count: ", res.matched_count)

# Call the find_one method by student_id 1007 and output the document to the terminal window.
print("\n*** Calling find_one() on student_id 1007 after update.")
student = students.find_one({"student_id": "1007"})
print(f'\n  Student ID: {student["student_id"]} \n  First Name: {student["first_name"]}  \n  Last Name:  {student["last_name"]} \n')
