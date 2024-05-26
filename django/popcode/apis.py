from hashlib import md5
import json
import random
import time
from bson import ObjectId
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
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


def login(req: HttpRequest):
    if not req.POST:
        return views.login(req)
    username = req.POST.get("username")
    password = req.POST.get("password")
    if not username or not password:
        return views.login(req)
    password = md5(password.encode("utf-8")).hexdigest()
    user = DB.users.find_one({"username": username})
    if not user:
        return views.login(req, {"error": "userNotFound"})
    if user["password"] != password:
        return views.login(req, {"error": "wrongPassword"})
    newToken = md5(str(random.random()).encode("utf-8")).hexdigest()
    DB.users.update_one(
        {"token": user["token"]},
        {"$set": {"lastLogin": time.time(), "token": newToken}},
    )
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


def signup(req: HttpRequest):
    username = req.POST.get("username")
    password = req.POST.get("password")
    email = req.POST.get("email")

    if not username or not password or not email:
        return redirect("/signup")
    print(username, password, email)
    if DB.users.find_one({"$or": [{"username": username}, {"email": email}]}):
        return redirect("/signup?error=usernameOrEmailExists")

    password = md5(password.encode("utf-8")).hexdigest()
    token = md5(str(random.random()).encode("utf-8")).hexdigest()
    DB.users.insert_one(
        {
            "username": username,
            "password": password,
            "email": email,
            "created": time.time(),
            "lastLogin": time.time(),
            "role": 0,
            "exp": 0,
            "coins": 0,
            "streak": 0,
            "progress": [],
            "token": token,
        }
    )
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


def editUser(req: HttpRequest):
    username = req.POST.get("username")
    password = req.POST.get("password")
    newPassword = req.POST.get("newPassword")
    email = req.POST.get("email")

    if not username or not password or not email:
        return views.settings(req)

    token = req.session.get("token")
    if not token:
        return views.settings(req, {"error": "tokenNotFound"})

    password = md5(password.encode("utf-8")).hexdigest()
    user = DB.users.find_one({"token": token, "password": password})
    if not user:
        return views.settings(req, {"error": "wrongPasswordOrToken"})

    if newPassword:
        newPassword = md5(newPassword.encode("utf-8")).hexdigest()
        DB.users.update_one(
            {"token": token},
            {"$set": {"username": username, "password": newPassword, "email": email}},
        )
    else:
        DB.users.update_one(
            {"token": token}, {"$set": {"username": username, "email": email}}
        )

    req.session["username"] = username
    req.session["email"] = email
    return views.settings(req)


"""
    Logout the user
    Redirects to /
"""


def logout(req: HttpRequest):
    req.session.pop("token")
    req.session.pop("username")
    req.session.pop("email")
    req.session.pop("admin")
    return redirect("/")


"""
    Create a new lesson with given title and description
    Redirects to / with success message lessonCreated
    Else redirects to / with error message :
    - notAdmin : If user is not admin
    - missingFields : If title or description is missing
"""


def createLesson(req: HttpRequest):
    user = getAdminUser(req)
    if not user:
        return redirect("/?error=notAdmin")
    title = req.POST.get("title")
    description = req.POST.get("description")
    if not title or not description:
        return redirect("/?error=missingFields")
    DB.lessons.insert_one(
        {
            "title": title,
            "description": description,
            "author": user["username"],
            "parts": [],
        }
    )
    return redirect("/?success=lessonCreated")


"""
    Delete a lesson with given lessonId
    Redirects to / with success message lessonDeleted
    Else redirects to / with error message :
    - notAdmin : If user is not admin
    - missingFields : If lessonId is missing
"""


def deleteLesson(req: HttpRequest):
    user = getAdminUser(req)
    if not user:
        return redirect("/?error=notAdmin")
    title = req.POST.get("title")
    if not title:
        return redirect("/?error=missingFields")
    DB.lessons.delete_one({"title": title})
    return redirect("/?success=lessonDeleted")


"""
    Create a new part with given lessonId, title and content
"""


def createPart(req: HttpRequest):
    if not req.POST:
        return redirect("/")
    user = getAdminUser(req)
    if not user:
        return redirect("/?error=notAdmin")
    lessonId = req.POST.get("lessonId")
    title = req.POST.get("title")
    description = req.POST.get("description")
    print(lessonId, title, description)
    if not lessonId or not title or not description:
        return redirect("/?error=missingFields")
    DB.lessons.update_one(
        {"title": lessonId},
        {
            "$push": {
                "parts": {"title": title, "description": description, "levels": []}
            }
        },
    )
    return redirect(f"/lesson/{lessonId}?success=partCreated")


"""
    Add a new level to a part with given lessonId, partIndex, title and content    
"""


def addLevel(req: HttpRequest):
    if not req.POST:
        return redirect("/?error=missingFields")
    type = req.POST.get("type")
    lessonId = req.POST.get("lessonId")
    partId = req.POST.get("partId")
    content = req.POST.get("content")
    if not type or not lessonId or not content:
        return redirect("/?error=missingFields")

    if type == "EXPL":
        DB.lessons.update_one(
            {"title": lessonId},
            {"$push": {f"parts.{partId}.levels": {"type": type, "content": content}}},
        )
    elif type == "CODE":
        lang, testcase, startcode = (
            req.POST.get("lang"),
            req.POST.get("testcase"),
            req.POST.get("startcode"),
        )
        DB.lessons.update_one(
            {"title": lessonId},
            {
                "$push": {
                    f"parts.{partId}.levels": {
                        "type": type,
                        "content": content,
                        "lang": lang,
                        "testcase": testcase,
                        "startcode": startcode,
                    }
                }
            },
        )
    elif type == "QUIZ":
        c1, c2, c3, c4, v1, v2, v3, v4 = (
            req.POST.get("c1"),
            req.POST.get("c2"),
            req.POST.get("c3"),
            req.POST.get("c4"),
            req.POST.get("v1"),
            req.POST.get("v2"),
            req.POST.get("v3"),
            req.POST.get("v4"),
        )
        answers = [
            {"content": v1, "valid": 1 if c1 is not None else 0},
            {"content": v2, "valid": 1 if c2 is not None else 0},
            {"content": v3, "valid": 1 if c3 is not None else 0},
            {"content": v4, "valid": 1 if c4 is not None else 0},
        ]
        DB.lessons.update_one(
            {"title": lessonId},
            {
                "$push": {
                    f"parts.{partId}.levels": {
                        "type": type,
                        "content": content,
                        "answers": answers,
                    }
                }
            },
        )
    return redirect(f"/lesson/{lessonId}/{partId}?success=levelAdded")


def viewPart(req: HttpRequest, title: str, part: int):
    lesson = DB.lessons.find_one({"title": title})
    if not lesson:
        return redirect("/")
    if part < 0 or part >= len(lesson["parts"]):
        return redirect(f"/lesson/{title}?error=partNotFound")
    p = lesson["parts"][part]
    return render(
        req,
        "popcode/part.html",
        context={"part": p, "lesson": lesson, "partIndex": part},
    )


def apiRun(req: HttpRequest):
    post = json.loads(req.body.decode("utf-8"))
    code = post["code"]
    lang = post["lang"]
    cr = CodeRunner(lang=lang, code=code)
    cr.run()
    return HttpResponse(json.dumps(cr.outputDict()), content_type="application/json")
    # return HttpResponse(json.dumps({"returnValue":"waffle > croffle"}),content_type="application/json")
