# Generated by Django 3.2 on 2021-05-03 01:57

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_profile_slug'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='relationship',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
