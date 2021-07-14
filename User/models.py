from django.db import models
from django.contrib.auth.models import User

import transliterate


def gen_slug(first, last):
    try:
        slug = transliterate.translit(f"{first}-{last}", reversed=True)
    except:
        slug = f"{first}-{last}"
    return slug


def upload_to_img(instance, filename):
    list_file = filename.split('.')
    return 'Profile/%s/%s/' % (instance.account.username, f'{gen_slug(instance.first_name, instance.last_name)}.{list_file[-1]}')


class Position(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    abbreviated_name = models.CharField('Сокращенное название', max_length=50)
    doc_name = models.CharField('Название для заявление или рапорта', max_length=150)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Profile(models.Model):
    """User"""
    STATUS = (
        ('Работает', 'Работает'),
        ('Уволен', 'Уволен'),
        ('В ожидании', 'В ожидании')
    )
    PAUL = (
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский')
    )
    last_name = models.CharField('Фамилия', max_length=20)
    first_name = models.CharField('Имя', max_length=20)
    sur_name = models.CharField('Отчество', max_length=20, null=True, blank=True)
    email = models.EmailField('Email')
    account = models.OneToOneField(User, verbose_name='Аккаунт', on_delete=models.PROTECT, related_name='profile', null=True, blank=True)
    position = models.ForeignKey(Position, verbose_name='Должность', on_delete=models.PROTECT, related_name='profile')
    body = models.TextField('О себе', null=True, blank=True)
    date_of_birth = models.DateField('День рождения')
    paul = models.CharField('Пол', max_length=10, choices=PAUL)
    tel_number = models.CharField('Номер телефона', max_length=50)
    itn = models.CharField('Идентификационный номер налогоплательщика (сокращенно ИНН)', max_length=70, unique=True)
    image = models.ImageField('Фото', upload_to=upload_to_img, null=True, blank=True)
    is_active = models.CharField('Статус', max_length=10, choices=STATUS, default="В ожидании")
    is_admin = models.BooleanField('Админ', default=False)
    is_statement = models.BooleanField('Заявление', default=False)
    is_report = models.BooleanField('Рапорт', default=False)
    created = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.sur_name if self.sur_name else ""}'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.sur_name if self.sur_name else ""}'

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'


class SettingsProfile(models.Model):
    """Settings"""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='settings')
    is_mail_inbox = models.BooleanField('Включить уведомление о новом документе', default=False)
    is_mail_movement = models.BooleanField('Включить уведомление о действие документах', default=False)
    is_mail_ad = models.BooleanField('Включить уведомление о новых событиях', default=False)

    objects = models.Manager()

    def __str__(self):
        return f'{self.profile.last_name} {self.profile.first_name}'

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'
