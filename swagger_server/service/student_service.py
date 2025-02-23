import os
import tempfile
from functools import reduce

# =========================================================
# Tiny DB
# =========================================================

from tinydb import TinyDB, Query

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)


def add(student=None):
    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        return 'already exists', 409

    doc_id = student_db.insert(student.to_dict())
    student.student_id = doc_id
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return 'not found', 404
    student['student_id'] = student_id
    print(student)
    return student


def delete(student_id=None):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return 'not found', 404
    student_db.remove(doc_ids=[int(student_id)])
    return student_id


# =========================================================
# Mongo DB
# =========================================================

# from pymongo import MongoClient
# from bson.objectid import ObjectId

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# client = MongoClient(MONGO_URI)
# db = client["devops-lab1"]
# students_collection = db["students"]


# def add(student=None):
#     res = students_collection.find_one({
#         "first_name": student.first_name,
#         "last_name": student.last_name
#     })
#     if res:
#         return 'already exists', 409

#     result = students_collection.insert_one(student.to_dict())
#     student.student_id = str(result.inserted_id)
#     return student.student_id


# def get_by_id(student_id=None, subject=None):

#     try:
#         student = students_collection.find_one({"_id": ObjectId(student_id)})
#         if not student:
#             return 'not found', 404

#         student['student_id'] = str(student['_id'])  # Convert ObjectId to string
#         del student['_id']  # Remove MongoDB's default ID field
#         return student
#     except Exception as e:
#         return f'Error: {str(e)}', 400

# def delete(student_id=None):
#     try:
#         result = students_collection.delete_one({"_id": ObjectId(student_id)})
#         if result.deleted_count == 0:
#             return 'not found', 404
#         return student_id
#     except Exception as e:
#         return f'Error: {str(e)}', 400
