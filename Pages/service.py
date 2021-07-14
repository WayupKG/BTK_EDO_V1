from django.core.mail import send_mail


def send(user_mail, content):
    send_mail(
        'Электронный документооборот',
        content,
        'edo.btk.kg@gmail.com',
        [user_mail],
        fail_silently=False
    )
