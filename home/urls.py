from django.contrib import admin
from django.urls import path, include
from home import views
urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login_page"),
    path("logout/", views.logout_page, name="logout_page"),
    path("register/", views.register_page, name="register_page"),
    path("todo/", views.todo, name="todo"),
    path("done/<id>/", views.done, name="done"),
    path("delete/<id>", views.delete, name="delete"),

]
