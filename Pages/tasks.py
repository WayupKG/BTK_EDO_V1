import Check_list.models as check_models
import Documents.models as doc_models
import User.models as user_models

from django.utils import timezone
from EdoMain.celery import app
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import time


@app.task
def send_mail(user_id, body):
    user = user_models.Profile.objects.get(pk=user_id)
    subject, from_email, to = 'Электронный документооборот', 'edo.btk.kg@gmail.com', user.email
    html_content = render_to_string('Email/mail_template.html', {'user': user, 'body': body})  #рендеринг с динамическим значением
    text_content = strip_tags(html_content)  # Удалите html-тег. Чтобы люди могли видеть хотя бы чистый текст.

    # Создайте электронное письмо и прикрепите также HTML-версию.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    # msg.attach_file('static/images/EDOBTK.svg')
    msg.send()


@app.task
def processing_database():
    date_now = timezone.now().strftime("%d-%m-%Y")
    documents = doc_models.Document.objects.filter(status='В процессе', type='Документ')
    try:
        for document in documents:
            if document.end_date.strftime("%d-%m-%Y") < date_now:
                for movement in document.movements.all():
                    if movement.status == 'В процессе':
                        if movement.answers.all():
                            for reply in movement.answers.all():
                                movement.status = 'Выполнено' if reply.status == 'Выполнено' or reply.status == 'В ожидании' else 'Не выполнено'
                        if not movement.answers.all():
                            movement.status = 'Не выполнено'
                    if movement.is_main_person:
                        if movement.appointment == 'Утверждаю' or movement.appointment == 'Согласен' or \
                           movement.appointment == 'Принято к исполнению' or movement.appointment == 'Принято к сведению':
                            document.status = 'Выполнено'
                            movement.status = 'Выполнено'
                        else:
                            if movement.answers.all():
                                for reply in movement.answers.all():
                                    movement.status = 'Выполнено' if reply.status == 'Выполнено' or reply.status == 'В ожидании' else 'Не выполнено'
                                    document.status = 'Выполнено' if reply.status == 'Выполнено' or reply.status == 'В ожидании' else 'Не выполнено'
                            if not movement.answers.all():
                                movement.status = 'Не выполнено'
                                document.status = 'Не выполнено'
                    movement.save()
                document.save()
            time.sleep(3)
        send_mail('Adikgk232323@gmail.com', 'Обработка базы данных был сделан')
    except:
        send_mail('Adikgk232323@gmail.com', 'Обработка базы данных не был сделан')


@app.task
def create_send_mail(user_id, password):
    user = user_models.Profile.objects.get(pk=user_id)
    subject, from_email, to = 'Электронный документооборот', 'edo.btk.kg@gmail.com', user.email
    html_content = render_to_string('Email/mail_create_user.html', {'user': user, 'password': password})  #рендеринг с динамическим значением
    text_content = strip_tags(html_content)  # Удалите html-тег. Чтобы люди могли видеть хотя бы чистый текст.

    # Создайте электронное письмо и прикрепите также HTML-версию.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    # msg.attach_file('static/images/EDOBTK.svg')
    msg.send()


@app.task
def create_check_list(document_id):
    doc = doc_models.Document.objects.get(pk=document_id)
    update_redirect, create_redirect = check_models.CheckList.objects.get_or_create(document=doc, defaults={'document': doc})
    if not create_redirect:
        update_redirect.document = doc
        update_redirect.save()
