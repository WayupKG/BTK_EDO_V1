from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.InboxDocView.as_view(), name="inbox"),
    path('inbox/remove/<slug:slug>/', views.remove_inbox, name="remove_inbox"),
    path('create/', views.create_doc_view, name="create_doc"),
    path('create/statement/', views.create_stat_view, name="create_statement"),
    path('create/raport/', views.create_raport_view, name="create_raport"),
    path('<slug:slug>/', views.doc_view, name="doc_view"),
    # path('sd/', views.shipped_doc_view, name='dovds')
]
