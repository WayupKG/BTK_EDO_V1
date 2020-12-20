import os
from django.db import models
from User.models import Profile, SettingsProfile
import Check_list
from django.utils.text import slugify
import transliterate

from Pages.tasks import send_mail


def gen_slug(number, name):
    try:
        slug = transliterate.translit(f"{number}-{name}", reversed=True)
    except:
        slug = f"{number}-{name}"

    new_slug = slugify(slug, allow_unicode=True)
    return new_slug


def create_number(id_doc):
    if id_doc < 10:
        number = f'20БТК00{id_doc}'
    elif 10 <= id_doc < 100:
        number = f'20БТК0{id_doc}'
    else:
        number = f'20БТК{id_doc}'
    return number


def upload_to_file(instance, filename):
    list_file = filename.split('.')
    return f'Documents/{instance.document.author.account.username}/{instance.document.number}/' \
           f'{list_file[0]}-{instance.document.number}.{list_file[-1]}/'


def upload_to_reply_file(instance, filename):
    list_file = filename.split('.')
    return f'Reply/{instance.reply.document.author.account.username}/{instance.reply.document.number}/' \
           f'{list_file[0]}-{instance.reply.document.number}.{list_file[-1]}/'


class In_Process_Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='В процессе').order_by('-created')


class Done_Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='Выполнено').order_by('-created')


class Not_Executed_Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='Не выполнено').order_by('-created')


class Document(models.Model):
    """Документ"""
    PURPOSES = (
        ('На утверждение', 'На утверждение'),
        ('На согласование', 'На согласование'),
        ('К исполнению', 'К исполнению'),
        ('К сведенью', 'К сведенью'),
    )
    STATUS = (
        ('Выполнено', 'Выполнено'),
        ('Не выполнено', 'Не выполнено'),
        ('В процессе', 'В процессе')
    )
    TYPE = (
        ('Документ', 'Документ'),
        ('Заявление', 'Заявление'),
        ('Рапорт', 'Рапорт'),
    )
    number = models.CharField('Номер документа', max_length=20, null=True, blank=True)
    author = models.ForeignKey(Profile, verbose_name='Автор', on_delete=models.PROTECT, related_name='author')
    name = models.CharField('Название документа', max_length=120)
    body = models.TextField('Описание документа')
    slug = models.SlugField(max_length=150)
    end_date = models.DateField(verbose_name='Срок исполнения', null=True, blank=True)
    purposes = models.CharField('Назначение', max_length=20, choices=PURPOSES, default='На утверждение')
    status = models.CharField('Статус', max_length=20, choices=STATUS, default='В процессе')
    type = models.CharField('Тип документа', max_length=20, choices=TYPE, default='Документ')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    in_process = In_Process_Manager()
    done = Done_Manager()
    not_executed = Not_Executed_Manager()

    def __str__(self):
        return f'{self.number}-{self.name}'

    def save(self, *args, **kwargs):
        try:
            doc = Document.objects.order_by('-pk')[0]
            try:
                self.number = create_number(int(self.pk))
                self.slug = gen_slug(self.number, self.name)
            except TypeError:
                self.number = create_number(int(doc.pk + 1))
                self.slug = gen_slug(self.number, self.name)
        except IndexError:
            try:
                self.number = create_number(int(self.pk))
                self.slug = gen_slug(self.number, self.name)
            except TypeError:
                self.number = create_number(1)
                self.slug = gen_slug(self.number, self.name)

        if self.status == 'Выполнено':
            doc = Document.objects.get(pk=self.pk)
            update_redirect, create_redirect = Check_list.models.CheckList.objects.get_or_create(document=doc, defaults={'document': doc})
            if not create_redirect:
                update_redirect.document = doc
                update_redirect.save()

        super(Document, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class FileDocument(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='files')
    file = models.FileField('Файлы', upload_to=upload_to_file, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return self.document.number

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Файл документа'
        verbose_name_plural = 'Файлы документов'


class MovementOfDocument(models.Model):
    """Движение документа"""
    VIEW = (
        ('Просмотрено', 'Просмотрено'),
        ('Не просмотрено', 'Не просмотрено'),
    )
    STATUS = (
        ('Выполнено', 'Выполнено'),
        ('Не выполнено', 'Не выполнено'),
        ('В процессе', 'В процессе')
    )
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='movements')
    responsible = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='movements')
    appointment = models.CharField('Движение', max_length=30, default='В ожидании')
    view = models.CharField('Просмотр', choices=VIEW, max_length=30, default='Не просмотрено')
    status = models.CharField('Статус документа', max_length=20, choices=STATUS, default='В процессе')
    is_main_person = models.BooleanField('Ответственный сотрудник', default=False)
    is_redirect = models.BooleanField('Перенаправлен сотруднику', default=False)
    is_open_reply = models.BooleanField('Можеть ли отправитьответь', default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    in_process = In_Process_Manager()
    done = Done_Manager()
    not_executed = Not_Executed_Manager()

    def save(self, *args, **kwargs):
        if self.view == 'Не просмотрено' and self.responsible.settings.is_mail_inbox:
            send_mail.delay(self.responsible.pk, f'Вам было отправлено документ с номером {self.document.number}')
        super(MovementOfDocument, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.document.number}-{self.responsible}'

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Движение документа'
        verbose_name_plural = 'Движения документов'


class ReplyDocument(models.Model):
    """Ответ на документ"""
    APPOINTMENT = (
        ('Утверждаю', 'Утверждаю'),
        ('Согласен', 'Согласен'),
        ('Не согласен', 'Не согласен'),
        ('Принято к исполнению', 'Принято к исполнению'),
        ('Принято к сведению', 'Принято к сведению'),
        ('В ожидании', 'В ожидании')
    )
    STATUS = (
        ('Принят', 'Принят'),
        ('Не принят', 'Не принят'),
        ('В ожидании', 'В ожидании')
    )
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='answers')
    movement = models.ForeignKey(MovementOfDocument, on_delete=models.CASCADE, related_name='answers')
    appointment = models.CharField('Движение', choices=APPOINTMENT, max_length=30, default='В ожидании')
    status = models.CharField('Статус ответа', max_length=20, choices=STATUS, default='В ожидании')
    description = models.TextField('Описание', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if self.status == 'В ожидании':
            body_doc = f'{self.movement.responsible} ответиль на документ с номером {self.document.number}.'
            body = False
            if self.document.author.settings.is_mail_movement:
                send_mail.delay(self.document.author.pk, body_doc)
        elif self.status == 'Принят':
            self.movement.status = 'Выполнено'
            self.movement.appointment = self.appointment
            self.movement.is_open_reply = False
            body = f'{self.document.author} принял ваш ответ. Ответ был отправлен на документ с номером {self.document.number}.'
        else:
            self.movement.status = 'Не принят'
            self.movement.is_open_reply = True
            body = f'{self.document.author} не принял ваш ответ. Ответ был отправлен на документ с номером {self.document.number}. ' \
                   f'Не забудьте отправить повторный ответ до конца срока исполнение.'
        self.movement.save()

        if self.movement.responsible.settings.is_mail_movement and body:
            send_mail.delay(self.movement.responsible.pk, body)
        super(ReplyDocument, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.movement)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class FileReplyDocument(models.Model):
    reply = models.ForeignKey(ReplyDocument, on_delete=models.CASCADE, related_name='files')
    file = models.FileField('Файл', upload_to=upload_to_reply_file)
    created = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return str(self.reply)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Файл ответа'
        verbose_name_plural = 'Файлы ответа'
