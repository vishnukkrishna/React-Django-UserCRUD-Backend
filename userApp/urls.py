from . import views
from django.urls import path

urlpatterns = [
    path("", views.new, name="views"),
]
