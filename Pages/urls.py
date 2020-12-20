
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="Home"),
    path('select/create/doc/', views.SelectCreateDocView.as_view(), name="select_doc"),
    path('shipped/', views.ShippedDocView.as_view(), name="ShippedDocView"),
    path('address/book/', views.AddressBookView.as_view(), name="address_book"),
]
