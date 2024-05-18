from django.http import HttpRequest
from django.shortcuts import render


def index(req: HttpRequest):
	return render(req,"popcode/index.html")

def homepage(req: HttpRequest):
	return render(req,"popcode/homepage.html")

def quiz(req: HttpRequest):
	return render(req,"popcode/quiz.html")

def signup(req: HttpRequest):
	return render(req,"popcode/signup.html")

def login(req: HttpRequest):
	return render(req,"popcode/login.html")