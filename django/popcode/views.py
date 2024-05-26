from email.policy import HTTP
import json
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .utils import getLessons, getUser

from .DB import DB


def index(req: HttpRequest):
    return render(
        req, "popcode/backendPlayground.html", context={"lessons": getLessons()}
    )


def homepage(req: HttpRequest):
    return render(req, "popcode/homepage.html")


def quiz(req: HttpRequest, title: str, part: int):
    l = DB.lessons.find_one({"title": title})
    if not l:
        return redirect("/")
    pls = l["parts"]
    if part > len(pls):
        return redirect("/")
    p = pls[part]
    if not p:
        return redirect("/")
    return render(req, "popcode/quiz.html", context={"part": p})


def login(req: HttpRequest, context={}):
    return render(req, "popcode/login.html")


def signup(req: HttpRequest, context={}):
    return render(req, "popcode/signup.html")


def settings(req: HttpRequest, context={}):
    return render(req, "popcode/settings.html")


def contact(req: HttpRequest, context={}):
    return render(req, "popcode/contact.html")


def profile(req: HttpRequest, username=""):
    if not username:
        user = getUser(req)
        if not user:
            return redirect("/")
        return render(req, "popcode/profile.html", context={"user": user})
    user = DB.users.find_one({"username": username})
    return render(
        req, "popcode/profile.html", context={"requestedname": username, "user": user}
    )


def readypage(req: HttpRequest):
    return render(req, "popcode/readypage.html")
