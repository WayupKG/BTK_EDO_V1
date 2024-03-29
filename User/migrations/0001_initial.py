# Generated by Django 3.0 on 2020-11-16 04:09

import User.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название')),
                ('abbreviated_name', models.CharField(max_length=30, verbose_name='Сокращенное название')),
                ('doc_name', models.CharField(max_length=60, verbose_name='Название для заявление или рапорта')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=20, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=20, verbose_name='Имя')),
                ('sur_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Отчество')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('body', models.TextField(blank=True, null=True, verbose_name='О себе')),
                ('date_of_birth', models.DateField(verbose_name='День рождения')),
                ('paul', models.CharField(choices=[('Мужской', 'Мужской'), ('Женский', 'Женский')], max_length=10, verbose_name='Пол')),
                ('tel_number', models.CharField(max_length=50, verbose_name='Номер телефона')),
                ('itn', models.IntegerField(unique=True, verbose_name='Идентификационный номер налогоплательщика (сокращенно ИНН)')),
                ('image', models.ImageField(blank=True, null=True, upload_to=User.models.upload_to_img, verbose_name='Фото')),
                ('is_active', models.CharField(choices=[('Работает', 'Работает'), ('Уволен', 'Уволен'), ('В ожидании', 'В ожидании')], default='В ожидании', max_length=10, verbose_name='Статус')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Админ')),
                ('is_statement', models.BooleanField(default=False, verbose_name='Заявление')),
                ('is_report', models.BooleanField(default=False, verbose_name='Рапорт')),
                ('created', models.DateTimeField(auto_now=True)),
                ('account', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Аккаунт')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='profile', to='User.Position', verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Анкета',
                'verbose_name_plural': 'Анкеты',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='SettingsProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_mail_inbox', models.BooleanField(default=False, verbose_name='Включить уведомление о новом документе')),
                ('is_mail_movement', models.BooleanField(default=False, verbose_name='Включить уведомление о действие документах')),
                ('is_mail_ad', models.BooleanField(default=False, verbose_name='Включить уведомление о новых событиях')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='User.Profile')),
            ],
            options={
                'verbose_name': 'Настройка',
                'verbose_name_plural': 'Настройки',
            },
        ),
    ]
