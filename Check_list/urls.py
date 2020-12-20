from django.urls import path
from . import views

urlpatterns = [
    path('', views.CheckListView.as_view(), name="check_list"),
    path('pdf-<str:key>/', views.check_list_pdf, name="check_list_pdf"),
]
