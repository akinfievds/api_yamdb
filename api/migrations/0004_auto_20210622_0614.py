# Generated by Django 3.0.5 on 2021-06-22 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210620_1411'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('pk',), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('pk',), 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
    ]