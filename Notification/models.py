from django.db import models
import Pages.tasks


class Notification(models.Model):
    """Уведомление"""
    VIEW = (
        ('Просмотрено', 'Просмотрено'),
        ('Не просмотрено', 'Не просмотрено'),
    )
    TYPE = (
        ('Простой', 'Простой'),
        ('Заявление', 'Заявление'),
        ('Рапорт', 'Рапорт'),
        ('Ответ', 'Ответ'),
        ('Чеклист', 'Чеклист'),
        ('Решение', 'Решение'),
        ('Другое', 'Другое'),
    )
    document = models.ForeignKey('Documents.Document', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    reply = models.ForeignKey('Documents.ReplyDocument', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    body = models.CharField('Описания',  max_length=900)
    user = models.ForeignKey('User.Profile', on_delete=models.CASCADE, related_name='notifications')
    view = models.CharField('Просмотр', choices=VIEW, max_length=50, default='Не просмотрено')
    type = models.CharField('Type', max_length=20, choices=TYPE, default='Простой', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if self.view == 'Не просмотрено' and self.user.settings.is_mail_ad:
            Pages.tasks.send_mail.delay(self.user.pk, self.body)
        super(Notification, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.document}-{self.body}'

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомлении'

