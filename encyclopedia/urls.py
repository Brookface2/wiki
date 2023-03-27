from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("wiki", views.index, name="index"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("random", views.randompage, name="randompage"),
    path("<page>", views.entry, name="pages" ),
    path("<page>/edit", views.editpage, name="edit"),
]
