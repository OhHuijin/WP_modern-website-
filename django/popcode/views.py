from django.http import HttpRequest
from django.shortcuts import render


def index(req: HttpRequest):
	return render(req,"popcode/index.html")