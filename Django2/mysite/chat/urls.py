# chat/urls.py
from django.urls import path

from . import views

# To call view
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]