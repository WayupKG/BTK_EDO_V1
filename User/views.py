from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import View, TemplateView
from django.contrib.auth.hashers import make_password
from Pages.tasks import create_send_mail
import transliterate
import random

from .models import Profile, SettingsProfile
from .forms import ProfileForm


@login_required
def profile_view(request, username):
    profile = get_object_or_404(Profile, account__username=username)
    if request.method == 'POST':
        data = request.POST.get
        if data('form_btn') == 'settings':
            profile.settings.is_mail_inbox = True if data('is_mail_inbox') == 'on' else False
            profile.settings.is_mail_movement = True if data('is_mail_movement') == 'on' else False
            profile.settings.is_mail_ad = True if data('is_mail_ad') == 'on' else False
            profile.settings.save()
            return redirect('Profile', username=request.user.username)
        elif data('form_btn') == 'profile':
            user = get_object_or_404(User, pk=request.user.pk)
            user.email = data('email')
            user.save()
            profile.first_name = data('first_name')
            profile.last_name = data('last_name')
            profile.sur_name = data('sur_name')
            profile.email = data('email')
            profile.tel_number = data('phone')
            profile.date_of_birth = data('date')
            profile.itn = data('itn')
            profile.body = data('body')
            profile.save()
            return redirect('Profile', username=request.user.username)
    return render(request, 'Pages/profile.html', {'profile': profile})


def registration(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        data = request.POST.get
        if data('password') == data('re_password'):
            if form.is_valid():
                profile = form.save(commit=False)
                user = User.objects.create(username=data('username'), email=data('email'), password=make_password(data('password')))
                profile.account = user
                profile.email = data('email')
                profile.save()
                SettingsProfile.objects.create(profile=profile)
                create_send_mail.delay(profile.pk, data('password'))
                return redirect('login')
        else:
            error = 'Пароль не совпадает'
    else:
        form = ProfileForm()
    return render(request, 'registration/register.html', {'form': form})
