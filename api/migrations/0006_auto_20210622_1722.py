# Generated by Django 3.0.5 on 2021-06-22 17:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210622_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Оценка отзыва может быть в диапазоне от 1 до 10'), django.core.validators.MaxValueValidator(10, message='Оценка отзыва может быть в диапазоне от 1 до 10')], verbose_name='Оценка отзыва'),
        ),
    ]