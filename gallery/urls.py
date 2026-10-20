from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("obras/", views.artwork_list, name="artwork_list"),
    path("obras/<slug:slug>/", views.artwork_detail, name="artwork_detail"),
    path("biografia/", views.biography, name="biography"),
    path("contato/", views.contact, name="contact"),
]
