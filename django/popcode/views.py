from email.policy import HTTP
import json
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .utils import getLessons, getUser

from .DB import DB


def backendPlayground(req: HttpRequest):
    """
    path /bp
    Backend Playground
    """
    return render(
        req, "popcode/backendPlayground.html", context={"lessons": getLessons()}
    )


def homepage(req: HttpRequest):
    """
    path /
    Redirects to dashboard if user is logged in, else to homepage
    """
    user = getUser(req)
    print(user)
    if user:
        return render(
            req,
            "popcode/readypage.html",
            context={"user": user, "lessons": getLessons()},
        )
    return render(req, "popcode/homepage.html")


def quiz(req: HttpRequest, title: str, part: int):
    l = DB.lessons.find_one({"title": title})
    if not l:
        return redirect("/?error=lesson_not_found")
    pls = l["parts"]
    if part > len(pls):
        return redirect("/?error=part_not_found")
    p = pls[part]
    if not p:
        return redirect("/?error=part_not_found")
    return render(req, "popcode/quiz.html", context={"part": p})


def login(req: HttpRequest, context={}):
    """
    path /login
    Redirects to dashboard if user is logged in, else to login page
    """
    user = getUser(req)
    if user:
        return redirect("/")
    return render(req, "popcode/login.html")


def signup(req: HttpRequest, context={}):
    """
    path /signup
    Redirects to dashboard if user is logged in, else to signup page
    """
    user = getUser(req)
    if user:
        return redirect("/")
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


def lesson(req: HttpRequest, title: str):
    lesson = DB.lessons.find_one({"title": title})
    if not lesson:
        return redirect("/")
    print(lesson)
    return render(req, "popcode/lesson.html", context={"lesson": lesson})
