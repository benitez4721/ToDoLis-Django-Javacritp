# Generated by Django 3.1.1 on 2020-10-04 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0007_team_user_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team_user',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
