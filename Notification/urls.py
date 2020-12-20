from django.urls import path
from . import views

urlpatterns = [
    path('notification/', views.NotificationView.as_view(), name='notification'),
    path('notification/remove/<int:id>/<slug:slug>/', views.remove_notification, name='remove_notification'),
    path('notification/single/<int:id>/<slug:slug>/', views.single_notification, name='single_notification'),
]
