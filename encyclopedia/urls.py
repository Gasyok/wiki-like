from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:TITLE>", views.wiki, name="wiki"),
    path('edit/<str:TITLE>', views.edit, name="edit"),
    path("new-page", views.add, name="add"),
    path("random", views.random_page, name="random")
]
