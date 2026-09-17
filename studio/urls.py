from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("work/", views.work, name="work"),
    path("work/<slug:slug>/", views.project, name="project"),
    path("contact/", views.contact, name="contact"),
    path("contact/thanks/", views.contact_success, name="contact_success"),
    path("appointments/book/", views.book_appointment, name="book_appointment"),
]
