""" 
Ryan Kite
CSD 310
Nov 18, 2021
Module 6
Assignment 6.3
Description: 
Deleting Documents
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

# Call the insert_one() method and Insert a new document into the pytech collection with student_id 1010.
# Frodo Baggins data document
print("\n*** Calling insert_one() on student_id: 1010")
ham = {
    "student_id": "1010",
    "first_name": "Ham",
    "last_name": "Bananas",
    "enrollments": [
        {
            "term": "Session 5",
            "gpa": "3.5",
            "start_date": "December 11, 2020",
            "end_date": "August 15, 2020",
            "courses": [
                {
                    "course_id": "CSD310",
                    "description": "Database Development and Use",
                    "instructor": "Professor Krasso",
                    "grade": "C"
                },
                {
                    "course_id": "CSD 320",
                    "description": "Programming with Java",
                    "instructor": "Professor Krasso",
                    "grade": "B"
                }
            ]
        }
    ]
}
ham_student_id = students.insert_one(ham).inserted_id
print("\n*** (created) student_id: [ham]", ham_student_id)

# Call the find_one() method and display the results to the terminal window.
print("\n*** Calling find_one() on student_id 1010 after creating.")
student = students.find_one({"student_id": "1010"})
print(f'\n  Student ID: {student["student_id"]} \n  First Name: {student["first_name"]}  \n  Last Name:  {student["last_name"]} \n')

# Call the delete_one() method by student_id 1010.
print("\n*** Calling delete_one() on student_id 1010.")
students.delete_one({"student_id": "1010"})

# Call the find() method and display the results to the terminal window.
student_list = students.find()
# # loop over collection 
print("\n*** Displaying all documents using .find() query")
for doc in student_list:
    print(f'\n  Student ID: {doc["student_id"]} \n  First Name: {doc["first_name"]}  \n  Last Name:  {doc["last_name"]}')


