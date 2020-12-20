from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration, name="registration"),
    path('profile/<username>/', views.profile_view, name="Profile"),
]
