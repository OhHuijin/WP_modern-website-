import json
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .utils import getLessons

from .DB import DB


def index(req: HttpRequest):
    return render(
        req, "popcode/backendPlayground.html", context={"lessons": getLessons()}
    )


def homepage(req: HttpRequest):
    return render(req, "popcode/homepage.html")


def quiz(req: HttpRequest, title: str, part: int):
    part = DB.lessons.find_one({"title": title})["parts"][part]
    if not part:
        return redirect("/")
    print("part is", part)
    return render(req, "popcode/quiz.html", context={"part": part})


def signup(req: HttpRequest, context={}):
    return render(req, "popcode/signup.html")


def settings(req: HttpRequest, context={}):
    return render(req, "popcode/settings.html")


def contact(req: HttpRequest, context={}):
    return render(req, "popcode/contact.html")


def login(req: HttpRequest, context={}):
    return render(req, "popcode/login.html", context=context)


def readypage(req: HttpRequest, context={}):
    return render(req, "popcode/readypage.html", context=context)


def profile(req: HttpRequest, context={}):
    return render(req, "popcode/backendPlayground.html", context=context)
