# Generated by Django 3.0.5 on 2021-06-17 20:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210617_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]
