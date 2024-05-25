from email.policy import HTTP
from django.http import HttpRequest

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
    return user if user.role == 1 else False