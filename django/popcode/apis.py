import datetime
from hashlib import md5
import json
import random
import time
from bson import ObjectId
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .utils import getAdminUser, getUser
from .DB import DB

from . import views
from .coderunner.CodeRunner import CodeRunner


def login(req: HttpRequest):
    """
    Try to login the user using given username and password.
    Redirects to / if successful
    Otherwise redirects to /login with error message.
    Automatically changes the user's token and updates lastLogin time.
    The streak is also updated if the user has not completed a lesson before yesterday.
    """
    username = req.POST.get("username")
    password = req.POST.get("password")
    if not username or not password:
        return redirect("/login?error=Missing username or password")
    password = md5(password.encode("utf-8")).hexdigest()
    user = DB.users.find_one({"username": username})
    if not user:
        return redirect("/login?error=Username doesn't exist")
    if user["password"] != password:
        return redirect("/login?error=Wrong password")
    newToken = md5(str(random.random()).encode("utf-8")).hexdigest()

    newStreak = user["streak"]

    todayStreak = False
    if user["lastActivity"] != 0:
        dt = datetime.datetime.fromtimestamp(user["lastActivity"]).date()
        yt = datetime.date.today() - datetime.timedelta(days=1)
        if dt < yt:
            newStreak = 0
        elif dt == datetime.date.today():
            todayStreak = True

    DB.users.update_one(
        {"token": user["token"]},
        {"$set": {"lastLogin": time.time(), "token": newToken, "streak": newStreak}},
    )
    req.session["token"] = newToken
    req.session["username"] = user["username"]
    req.session["email"] = user["email"]
    req.session["admin"] = user["role"] == 1
    req.session["streak"] = user["streak"]
    req.session["todayStreak"] = todayStreak
    return redirect(f"/?success=Welcome back {user['username']}!")


def signup(req: HttpRequest):
    """
    Create a new user with given username, password and email.
    Redirects to / if successful
    Otherwise redirects to /signup with error message.
    Username and email are unique.
    """
    username = req.POST.get("username")
    password = req.POST.get("password")
    email = req.POST.get("email")

    if not username or not password or not email:
        return redirect("/signup?error=Missing username, password or email")
    print(username, password, email)
    if DB.users.find_one({"$or": [{"username": username}, {"email": email}]}):
        return redirect("/signup?error=User with this username or email already exists")

    password = md5(password.encode("utf-8")).hexdigest()
    token = md5(str(random.random()).encode("utf-8")).hexdigest()
    DB.users.insert_one(
        {
            "username": username,  # username is unique
            "password": password,
            "email": email,  # email is unique
            "created": time.time(),
            "lastLogin": time.time(),
            "lastActivity": 0,  # last activity time (updates to time.time() when completing a lesson)
            "role": 0,
            "exp": 0,
            "coins": 0,
            "streak": 0,
            "progress": {},
            "token": token,
        }
    )
    req.session["token"] = token
    req.session["username"] = username
    req.session["email"] = email
    req.session["admin"] = False
    req.session["streak"] = 0
    req.session["todayStreak"] = False
    return redirect(f"/?success=Welcome to PopCode, {username}!")


def editUser(req: HttpRequest):
    """
    Edit the user's profile with given username, password, email and newPassword.
    Applies changes if password and token are correct.
    Redirects to / with success message.
    Otherwise redirects to /settings with error message.
    """
    username = req.POST.get("username")
    password = req.POST.get("password")
    newPassword = req.POST.get("newPassword")
    email = req.POST.get("email")

    if not username or not password or not email:
        return redirect("/settings?error=Missing username, actual password or email")

    token = req.session.get("token")
    if not token:
        return redirect("/settings?error=Token not found in session")

    password = md5(password.encode("utf-8")).hexdigest()
    user = DB.users.find_one({"token": token, "password": password})
    if not user:
        return redirect("/settings?error=Wrong password or invalid token")

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
    return redirect("/?success=Profile updated!")


def logout(req: HttpRequest):
    """
    Logout the user, cleaning the session.
    Redirects to /
    """
    req.session.pop("token")
    req.session.pop("username")
    req.session.pop("email")
    req.session.pop("admin")
    return redirect("/?success=Logged out successfully!")


def createLesson(req: HttpRequest):
    """
    Create a new lesson with given title and description
    The user must be an admin and the fields must not be empty.
    We assume
    Always redirect to / with a message
    """
    user = getAdminUser(req)
    if not user:
        return redirect("/?error=You are not an admin")
    title = req.POST.get("title")
    description = req.POST.get("description")
    if not title or not description:
        return redirect("/?error=Some fields are missing")
    DB.lessons.insert_one(
        {
            "title": title,
            "description": description,
            "author": user["username"],
            "parts": [],
        }
    )
    return redirect("/?success=Lession created successfully!")


def deleteLesson(req: HttpRequest):
    """
    Delete a lesson with given title
    Requires admin rights
    Always redirect to / with a message
    """
    user = getAdminUser(req)
    if not user:
        return redirect("/?error=You are not an admin")
    title = req.POST.get("title")
    if not title:
        return redirect("/?error=Some fields are missing")
    DB.lessons.delete_one({"title": title})
    return redirect("/?success=Lession deleted successfully!")


def createPart(req: HttpRequest):
    """
    Create a new part with given lessonId, title and content
    """
    if not req.POST:
        return redirect("/")
    user = getAdminUser(req)
    if not user:
        return redirect("/?error=You are not an admin")
    lessonId = req.POST.get("lessonId")
    title = req.POST.get("title")
    description = req.POST.get("description")
    print(lessonId, title, description)
    if not lessonId or not title or not description:
        return redirect("/?error=Some fields are missing")
    DB.lessons.update_one(
        {"title": lessonId},
        {
            "$push": {
                "parts": {"title": title, "description": description, "levels": []}
            }
        },
    )
    return redirect(f"/lesson/{lessonId}?success=partCreated")


def addLevel(req: HttpRequest):
    """
    Add a new level to a part with given lessonId, partIndex, title and content
    """
    type = req.POST.get("type")
    lessonId = req.POST.get("lessonId")
    partId = req.POST.get("partId")
    content = req.POST.get("content")
    if not type or not lessonId or not content:
        return redirect("/?error=Some fields are missing")

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
    return redirect(f"/lesson/{lessonId}/{partId}?success=Level added !")


def viewPart(req: HttpRequest, title: str, part: int):
    """
    View a part of a lesson with given title and part index
    """
    lesson = DB.lessons.find_one({"title": title})
    if not lesson:
        return redirect("/")
    if part < 0 or part >= len(lesson["parts"]):
        return redirect(f"/lesson/{title}?error=Invalid part index")
    p = lesson["parts"][part]
    return render(
        req,
        "popcode/part.html",
        context={"part": p, "lesson": lesson, "partIndex": part},
    )


def apiRun(req: HttpRequest):
    """
    Run the given code in the given language
    """
    post = json.loads(req.body.decode("utf-8"))
    code = post["code"]
    lang = post["lang"]
    cr = CodeRunner(lang=lang, code=code)
    cr.run()
    cr.cleanAll()
    return HttpResponse(json.dumps(cr.outputDict()), content_type="application/json")
    # return HttpResponse(json.dumps({"returnValue":"waffle > croffle"}),content_type="application/json")


def finishLesson(req: HttpRequest):
    """
    Finish a lesson with given title and part index
    Updates the user's progress and streak
    Redirects to / with a message
    """
    user = getUser(req)
    if not user:
        return redirect("/?error=You are not logged in")

    title = req.GET.get("title")
    part = req.GET.get("part")
    if not title or not part:
        return redirect("/?error=Couldn't update progress, missing fields")

    lesson = DB.lessons.find_one({"title": title})
    if not lesson:
        return redirect("/?error=Lesson not found")

    part = int(part)
    if part < 0 or part >= len(lesson["parts"]):
        return redirect("/?error=Invalid part index")

    if title in user["progress"]:
        part = max(part, user["progress"][title])

    today = datetime.date.today()
    last_activity = datetime.datetime.fromtimestamp(user["lastActivity"]).date()

    newStreak = user["streak"] + 1
    if last_activity >= today:
        newStreak = 1

    DB.users.update_one(
        {"token": user["token"]},
        {
            "$set": {
                f"progress.{title}": part,
                "lastActivity": time.time(),
                "streak": newStreak,
            }
        },
    )

    req.session["todayStreak"] = True
    req.session["streak"] = newStreak
    return redirect(f"/?success=Congrats for finishing {title} part {part}!")
