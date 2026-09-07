from django.urls import path
from .views import letter_list

urlpatterns = [
    path("letters/", letter_list, name="letter-list"),
]