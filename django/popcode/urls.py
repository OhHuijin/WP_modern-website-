"""
URL configuration for popcode project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import views, apis

urlpatterns = [
    # General views
    path("", views.homepage, name="homepage"),
    path("quiz", views.quiz, name="quiz"),
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("settings", views.settings, name="settings"),
    path("profile", views.profile, name="profile"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("lesson/<str:title>", views.lesson, name="lesson"),
    path("lesson/<str:title>/<int:part>", views.quiz, name="part"),
    path("contact", views.contact, name="contact"),
    # Backend Playground
    path("bp", views.backendPlayground, name="bp"),
    path("bp/<str:title>", views.lesson, name="bpLesson"),
    path("bp/<str:title>/<int:part>", apis.viewPart, name="bpPart"),
    # Backend endpoints
    path("api/login", apis.login, name="apiLogin"),
    path("api/signup", apis.signup, name="apiSignup"),
    path("api/logout", apis.logout, name="apiLogout"),
    path("api/editUser",apis.editUser,name='apiEditUser'),
    path("api/createLesson", apis.createLesson, name="apiCreateLesson"),
    path("api/deleteLesson", apis.deleteLesson, name="apiDeleteLesson"),
    path("api/createPart", apis.createPart, name="apiCreatePart"),
    path("api/addLevel", apis.addLevel, name="apiAddLevel"),
    path("api/run", apis.apiRun, name="apiRun"),
    # Admin
    path("admin/", admin.site.urls),
]

# urlpatterns = [
# 	path('',views.index,name="index"),
#     path('homepage',views.homepage,name="homepage"),
#     path('quiz',views.quiz,name="quiz"),
#     path('signup',apis.signup,name="signup"),
#     path('user',views.signup,name="user"),
#     path('login',apis.login,name="login"),

# 	path('api/run',apis.apiRun,name="apiRun"),
#     path('admin/', admin.site.urls),
#     path("profile",apis.editUser,name="profile"),
#     path("logout",apis.logout,name="logout"),
#     path("createLesson",apis.createLesson,name="createLesson"),
#     path("deleteLesson",apis.deleteLesson,name="deleteLesson"),
#     path("createPart",apis.createPart,name="createPart"),
#     path("lesson/<str:title>",apis.viewLesson,name="lesson"),
#     path("lesson/<str:title>/<int:part>",apis.viewPart,name="part")
# ]
