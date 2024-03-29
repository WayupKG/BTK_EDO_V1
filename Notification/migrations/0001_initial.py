# Generated by Django 3.0 on 2020-11-16 04:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
        ('Documents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=150, verbose_name='Описания')),
                ('view', models.CharField(choices=[('Просмотрено', 'Просмотрено'), ('Не просмотрено', 'Не просмотрено')], default='Не просмотрено', max_length=50, verbose_name='Просмотр')),
                ('type', models.CharField(choices=[('Простой', 'Простой'), ('Заявление', 'Заявление'), ('Рапорт', 'Рапорт'), ('Ответ', 'Ответ'), ('Чеклист', 'Чеклист'), ('Другое', 'Другое')], default='Простой', max_length=20, null=True, verbose_name='Type')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='Documents.Document')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='Documents.ReplyDocument')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='User.Profile')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомлении',
                'ordering': ('-created',),
            },
        ),
    ]
