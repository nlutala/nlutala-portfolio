"""
Allows for calling the different views by mapping it to a URL.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("projects", views.projects, name="projects"),
    path("projects/", views.projects, name="projects"),
    path("projects/pdf-merger", views.pdf_merger, name="pdf-merger"),
    path("projects/pdf-merger/", views.pdf_merger, name="pdf-merger"),
    path(
        "projects/password-generator",
        views.password_generator,
        name="password-generator",
    ),
    path(
        "projects/password-generator/",
        views.password_generator,
        name="password-generator",
    ),
    path("projects/hangman", views.hangman_template, name="hangman_template"),
    path("projects/hangman/", views.hangman_template, name="hangman_template"),
    path("projects/tic-tac-toe", views.tic_tac_toe, name="tic_tac_toe"),
    path("projects/tic-tac-toe/", views.tic_tac_toe, name="tic_tac_toe"),
]
