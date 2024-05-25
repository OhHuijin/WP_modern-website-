from django.http import HttpRequest
from django.shortcuts import render

from .utils import getLessons

from .DB import DB


def index(req: HttpRequest):
    return render(req,"popcode/backendPlayground.html",context={"lessons":getLessons()})

def homepage(req: HttpRequest):
    return render(req,"popcode/homepage.html")

def quiz(req: HttpRequest):
    return render(req,"popcode/quiz.html")

def signup(req: HttpRequest,context={}):
    return render(req,"popcode/signup.html")

def login(req: HttpRequest,context={}):
    return render(req,"popcode/login.html",context=context)

def readypage(req: HttpRequest,context={}):
    return render(req,"popcode/readypage.html",context=context)

def profile(req: HttpRequest,context={}):
    return render(req,"popcode/backendPlayground.html",context=context)