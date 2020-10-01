
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("main", views.main, name = "main"),

    path("register", views.register_view, name = "register"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),

    path("add_task", views.add_task, name = "add_task"),
    path("check/<int:id>", views.check, name = "check"),
    path("delete/<int:id>", views.delete, name = "delete")
]