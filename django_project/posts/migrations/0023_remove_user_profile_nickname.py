# Generated by Django 3.0.5 on 2020-12-05 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0022_auto_20201205_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_nickname',
        ),
    ]