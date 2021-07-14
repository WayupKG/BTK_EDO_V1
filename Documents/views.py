from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import View, TemplateView
from django.contrib.auth.hashers import make_password

from .models import Document, MovementOfDocument, FileDocument, ReplyDocument, FileReplyDocument
from Notification.models import Notification
from Check_list.models import CheckList
from User.models import Profile
from .forms import CreateDocumentForm, CreateStatementForm, CreateReportForm

import random


@login_required()
def create_doc_view(request):
    staffs = Profile.objects.filter(is_active='Работает')
    if request.method == 'POST':
        form = CreateDocumentForm(request.POST)
        person = request.POST.get('person')
        if form.is_valid():
            doc = form.save(commit=False)
            doc.author = request.user.profile
            doc.save()
            main_person = 0
            for file in request.FILES.getlist('files'):
                FileDocument.objects.create(document=doc, file=file)
            for staff in request.POST.getlist('responsible'):
                user_profile = Profile.objects.get(pk=staff)
                if staff == person:
                    main_person += 1
                    MovementOfDocument.objects.create(document=doc, responsible=user_profile, is_main_person=True)
                else:
                    MovementOfDocument.objects.create(document=doc, responsible=user_profile, is_main_person=False)
            if main_person == 0:
                user_profile = Profile.objects.get(pk=person)
                MovementOfDocument.objects.create(document=doc, responsible=user_profile, is_main_person=True)
            return redirect('doc_view', doc.slug)
    else:
        form = CreateDocumentForm()
    return render(request, 'Document/CreateDoc.html', {'form': form, 'staffs': staffs})


@login_required()
def create_stat_view(request):
    staffs = Profile.objects.filter(is_admin=True, is_active='Работает')
    if request.method == 'POST':
        form = CreateStatementForm(request.POST)
        if form.is_valid():
            statement = form.save(commit=False)
            statement.author = request.user.profile
            statement.type = 'Заявление'
            statement.save()
            user = Profile.objects.get(pk=int(request.POST.get('person')))
            MovementOfDocument.objects.create(
                document=statement, responsible=user)
            return redirect('doc_view', statement.slug)
    else:
        form = CreateStatementForm()
    return render(request, 'Document/CreateStatement.html', {'form': form, 'staffs': staffs})


@login_required()
def create_raport_view(request):
    staffs = Profile.objects.filter(is_admin=True, is_active='Работает')
    if request.method == 'POST':
        form = CreateReportForm(request.POST)
        if form.is_valid():
            raport = form.save(commit=False)
            raport.author = request.user.profile
            raport.type = 'Рапорт'
            raport.save()
            user = Profile.objects.get(pk=int(request.POST.get('person')))
            MovementOfDocument.objects.create(
                document=raport, responsible=user)
            return redirect('doc_view', raport.slug)
    else:
        form = CreateReportForm()
    return render(request, 'Document/CreateRaport.html', {'form': form, 'staffs': staffs})


class InboxDocView(LoginRequiredMixin, TemplateView):
    template_name = 'Document/inbox.html'

    def get(self, request, *args, **kwargs):
        docs = MovementOfDocument.objects.filter(responsible=request.user.profile)
        return render(request, self.template_name, {'docs': docs})


@login_required()
def remove_inbox(request, slug):
    try:
        doc = get_object_or_404(
            MovementOfDocument, document__slug=slug, responsible=request.user.profile)
        doc.view = 'Просмотрено'
        doc.save()
        return redirect('doc_view', slug)
    except:
        return redirect('doc_view', slug)


def create_notification(movement, appointment):
    body = ''
    if appointment == 'Утверждаю':
        body = f'{movement.responsible.position} - {movement.responsible} утвердил ваш документ.'
    elif appointment == 'Согласен':
        body = f'{movement.responsible.position} - {movement.responsible} согласен с вашим документом.'
    elif appointment == 'Не согласен':
        body = f'{movement.responsible.position} - {movement.responsible} не согласен с вашим документом.'
    elif appointment == 'Принято к исполнению':
        body = f'{movement.responsible.position} - {movement.responsible} принял к исполнению.'
    elif appointment == 'Принято к сведенью':
        body = f'{movement.responsible.position} - {movement.responsible} принял к сведенью.'
    return body


@login_required()
def doc_view(request, slug):
    doc = get_object_or_404(Document, slug=slug)
    staffs = Profile.objects.filter(is_active='Работает')
    try:
        movement = get_object_or_404(MovementOfDocument, document=doc, responsible=request.user.profile)
    except:
        movement = False
    if request.method == 'POST':
        data = request.POST.get
        redirect_person = data('redirect') if data('redirect') else False
        btn_reply = data('btn_reply') if data('btn_reply') else False
        appointment = data('appointment')
        print(request.POST)
        if movement.document.type != 'Документ' or movement.document.end_date.strftime("%d-%m-%Y") >= timezone.now().strftime("%d-%m-%Y"):
            if btn_reply == 'Выполнено':
                movement.status = 'Выполнено'
                doc.status = 'Выполнено'
            elif btn_reply == 'Не выполнено':
                movement.status = 'Не выполнено'
                doc.status = 'Не выполнено'
            else:
                reply = ReplyDocument.objects.create(document=doc, movement=movement, description=data('body'), appointment=appointment)
                for file in request.FILES.getlist('files'):
                    FileReplyDocument.objects.create(reply=reply, file=file)
                Notification.objects.create(document=doc, user=movement.document.author, reply=reply,
                                            body=create_notification(movement, appointment), type='Ответ')
                if redirect_person:
                    movement.is_main_person = False
                    user_profile = Profile.objects.get(pk=redirect_person)
                    update_redirect, create_redirect = MovementOfDocument.objects.get_or_create(document=doc, is_main_person=True, is_redirect=True,
                                                                                                defaults={'document': doc, 'responsible': user_profile, 'is_main_person': True, 'is_redirect': True})
                    if not create_redirect:
                        update_redirect.responsible = user_profile
                        update_redirect.save()
            movement.is_open_reply = False
            doc.save(), movement.save()
            error = False
            return redirect('doc_view', slug=doc.slug)
        else:
            error = 'Срок исполнение документа истек'
            return redirect('doc_view', slug=doc.slug)
    else:
        error = False
    return render(request, 'Document/Doc_Details.html', {'doc': doc, 'movement': movement, 'error': error, 'staffs': staffs})
