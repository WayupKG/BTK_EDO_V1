from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import View, TemplateView
from django.contrib.auth.hashers import make_password

from Documents.models import Document, MovementOfDocument
from User.models import Profile

import random


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'Pages/index.html'


class SelectCreateDocView(LoginRequiredMixin, TemplateView):
    template_name = 'Document/SelectCreateDoc.html'


class ShippedDocView(TemplateView):
    template_name = 'Document/Shipped.html'

    def get(self, request, *args, **kwargs):
        docs = Document.objects.filter(author=request.user.profile)
        return render(request, self.template_name, {'docs': docs})


class AddressBookView(LoginRequiredMixin, TemplateView):
    template_name = 'Pages/address_book.html'

    def get(self, request, *args, **kwargs):
        profiles = Profile.objects.all()
        return render(request, self.template_name, {'profiles': profiles})