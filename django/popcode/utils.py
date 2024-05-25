from email.policy import HTTP
from django.http import HttpRequest
from .DB import DB
from django import template

"""
    Returns the user object if user is logged in.
    Else returns False
"""
def getUser(req:HttpRequest):
    if "token" not in req.session:
        return False
    return DB.users.find_one({"token":req.session["token"]})
 
"""
    Returns the user object if user is logged in and is admin.
    Else returns False
"""
def getAdminUser(req:HttpRequest):
    user = getUser(req)
    if not user:
        return False
    return user if user["role"] == 1 else False

"""
    Get lessons, and expose their id
"""
def getLessons():
    lessons = DB.lessons.find()
    lessons_list = []

    for lesson in lessons:
        lesson_dict = dict(lesson)
        lesson_dict['id'] = lesson_dict['_id']
        lessons_list.append(lesson_dict)
    
    return lessons_list