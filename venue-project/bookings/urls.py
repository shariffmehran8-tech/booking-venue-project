from django.urls import path
from . import views

urlpatterns = [
    path("", views.space_list, name="space_list"),
    path("space/<int:pk>/", views.space_detail, name="space_detail"),
    path("space/<int:pk>/book/", views.book_space, name="book_space"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("booking/<int:pk>/cancel/", views.cancel_booking, name="cancel_booking"),
    path("signup/", views.signup, name="signup"),
]
