# Generated by Django 3.2 on 2021-05-02 12:59

from django.db import migrations, models
import profanity.validators


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20210501_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(max_length=500, validators=[profanity.validators.validate_is_profane]),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(validators=[profanity.validators.validate_is_profane]),
        ),
    ]