from hashlib import md5
import json
import random
import time
from bson import ObjectId
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from .utils import getAdminUser
from .DB import DB

from . import views
from .coderunner.CodeRunner import CodeRunner

"""
    Tries to login the user using given username and password.
    Redirect to / if successful
    Else redirect to /login with error message :
    - missingFields : If username or password is missing
    - userNotFound : If user with given username is not found
    - wrongPassword : If password is wrong
"""
def login(req:HttpRequest):
    username = req.POST["username"]
    password = req.POST["password"]
    if not username or not password:
        return views.login(req)
    password = md5(password.encode("utf-8")).hexdigest()
    user = DB.users.find_one({"username":username})
    if not user:
        return views.login(req,{"error":"userNotFound"})
    if user["password"] != password:
        return views.login(req, {"error":"wrongPassword"})
    newToken = md5(str(random.random()).encode("utf-8")).hexdigest()
    DB.users.update_one({"token":user["token"]},{"$set":{"lastLogin":time.time(), "token":newToken}})
    req.session["token"] = newToken
    req.session["username"] = user["username"]
    req.session["email"] = user["email"]
    req.session["admin"] = user["role"] == 1
    return redirect("/")
    
"""
    Tries to signup the user using given username, password and email.
    Redirects to / if successful
    Else redirects to /signup with error message :
    - usernameOrEmailExists : If username or email is already taken
"""
def signup(req:HttpRequest):
    username = req.POST["username"]
    password = req.POST["password"]
    email = req.POST["email"]
    
    if not username or not password or not email:
        return views.signup(req)
    
    if DB.users.find_one({"$or":[{"username":username},{"email":email}]}):
        return views.signup(req, {"error":"usernameOrEmailExists"})
    
    password = md5(password.encode("utf-8")).hexdigest()
    token = md5(str(random.random()).encode("utf-8")).hexdigest()
    DB.users.insert_one({
        "username":username,
        "password":password,
        "email":email,
        "created":time.time(),
        "lastLogin":time.time(),
        "role":0,
        "exp":0,
        "coins":0,
        "streak":0,
        "progress":[],
        "token":token
    })
    req.session["token"] = token
    req.session["username"] = username
    req.session["email"] = email
    req.session["admin"] = False
    return redirect("/")
    
"""
    Edit the user information, with given username, password, newPassword and email.
    Redirects to /profile if successful
    Else redirects to /profile with error message :
    - wrongPasswordOrToken : If password is wrong, or token is invalid
"""
def editUser(req:HttpRequest):
    username = req.POST["username"]
    password = req.POST["password"]
    newPassword = req.POST["newPassword"]
    email = req.POST["email"]
    
    if not username or not password or not email:
        return views.profile(req)
    
    token = req.session.get("token")
    if not token:
        return views.profile(req, {"error":"tokenNotFound"})
    
    password = md5(password.encode("utf-8")).hexdigest()
    print("password is ",password)
    print("token is ",token)
    user = DB.users.find_one({"token":token,"password":password})
    if not user:
        return views.profile(req, {"error":"wrongPasswordOrToken"})
    
    if newPassword:
        newPassword = md5(newPassword.encode("utf-8")).hexdigest()
        DB.users.update_one({"token":token},{"$set":{"username":username,"password":newPassword,"email":email}})
    else:
        DB.users.update_one({"token":token},{"$set":{"username":username,"email":email}})
    
    req.session["username"] = username
    req.session["email"] = email
    return views.profile(req)

"""
    Logout the user
    Redirects to /
"""
def logout(req:HttpRequest):
    req.session.pop("token")
    req.session.pop("username")
    return redirect("/")

"""
    Create a new lesson with given title and description
    Redirects to / with success message lessonCreated
    Else redirects to / with error message :
    - notAdmin : If user is not admin
    - missingFields : If title or description is missing
"""
def createLesson(req:HttpRequest):
    user = getAdminUser(req)
    if not user:
        return redirect("/?error=notAdmin")
    title = req.POST["title"]
    description = req.POST["description"]
    if not title or not description:
        return redirect("/?error=missingFields")
    DB.lessons.insert_one({
        "title":title,
        "description":description,
        "author":user["username"],
        "chapters":[]
    })
    return redirect("/?success=lessonCreated")

"""
    Delete a lesson with given lessonId
    Redirects to / with success message lessonDeleted
    Else redirects to / with error message :
    - notAdmin : If user is not admin
    - missingFields : If lessonId is missing
"""
def deleteLesson(req:HttpRequest):
    user = getAdminUser(req)
    if not user:
        return redirect("/?error=notAdmin")
    lessonId = req.POST["id"]
    if not lessonId:
        return redirect("/?error=missingFields")
    DB.lessons.delete_one({"_id":ObjectId(lessonId)})
    return redirect("/?success=lessonDeleted")
    
    

def apiRun(req:HttpRequest):
    post = json.loads(req.body.decode("utf-8"))
    code = post["code"]
    lang = post["lang"]
    cr = CodeRunner(lang=lang,code=code)
    cr.run()
    return HttpResponse(json.dumps(cr.outputDict()),content_type="application/json")
    #return HttpResponse(json.dumps({"returnValue":"waffle > croffle"}),content_type="application/json")