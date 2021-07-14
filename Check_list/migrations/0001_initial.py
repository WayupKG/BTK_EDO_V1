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
            name='CheckList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер чек листа')),
                ('status', models.CharField(blank=True, choices=[('Выполнено', 'Выполнено'), ('Не выполнено', 'Не выполнено')], max_length=20, null=True)),
                ('private_key', models.CharField(default=0, max_length=180)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='check_lists', to='User.Profile')),
                ('document', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='check_lists', to='Documents.Document')),
            ],
            options={
                'verbose_name': 'Чек лист',
                'verbose_name_plural': 'Чек листы',
                'ordering': ('-created',),
            },
        ),
    ]
