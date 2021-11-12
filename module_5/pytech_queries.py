""" 
Ryan Kite
CSD 310
Nov 11, 2021
Module 5
Assignment 5.3
Description: 
Collection Queries II
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

# find all students in collection 
student_list = students.find({})

# loop over collection 
print("Displaying all documents for .find() [all students] query")
for doc in student_list:
    print(f'\n  Student ID: {doc["student_id"]} \n  First Name: {doc["first_name"]}  \n  Last Name:  {doc["last_name"]} \n')

# use the find_one for displaying one student
print("Displaying document for one find_one() [single student] query")
student = students.find_one({"student_id": "1007"})
print(f'\n  Student ID: {student["student_id"]} \n  First Name: {student["first_name"]}  \n  Last Name:  {student["last_name"]} \n')