from django.db import models
from Documents.models import Document
from Notification.models import Notification
from User.models import Profile, SettingsProfile
import random


def create_number(id_doc):
    if id_doc < 10:
        number = f'01/00{id_doc}'
    elif 10 <= id_doc < 100:
        number = f'01/0{id_doc}'
    else:
        number = f'01/{id_doc}'
    return number


class CheckList(models.Model):
    STATUS = (
        ('Выполнено', 'Выполнено'),
        ('Не выполнено', 'Не выполнено'),
    )
    number = models.CharField('Номер чек листа', max_length=20, null=True, blank=True)
    document = models.OneToOneField(Document, on_delete=models.PROTECT, related_name='check_lists')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='check_lists', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, null=True, blank=True)
    private_key = models.CharField(max_length=180, default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        chars = 'abcd465efgh7ijk5lno4165pqrs7tdfhh4gdfsjk456saad5ad6489fuv8wx9yz12378440'
        key = ''
        for i in range(12):
            key += random.choice(chars)
        self.private_key = key
        self.author = self.document.author
        self.status = self.document.status
        try:
            check = CheckList.objects.order_by('-pk')[0]
            try:
                self.number = create_number(int(self.pk))
            except TypeError:
                self.number = create_number(int(check.pk + 1))
        except IndexError:
            try:
                self.number = create_number(int(self.pk))
            except TypeError:
                self.number = create_number(1)
        body = f'Создан чек лист на документ с номером {self.document.number}'
        Notification.objects.create(document=self.document, user=self.author, view='Не просмотрено', body=body, type='Чеклист')
        super(CheckList, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Чек лист'
        verbose_name_plural = 'Чек листы'
