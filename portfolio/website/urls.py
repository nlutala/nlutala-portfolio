'''
Allows for calling the different views by mapping it to a URL.
'''
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
