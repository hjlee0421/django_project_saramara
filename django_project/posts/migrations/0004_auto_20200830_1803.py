# Generated by Django 3.0.8 on 2020-08-30 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20200830_1729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='mara_cnt',
        ),
        migrations.RemoveField(
            model_name='post',
            name='sara_cnt',
        ),
        migrations.AlterField(
            model_name='post',
            name='mara',
            field=models.TextField(default=' ', null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='sara',
            field=models.TextField(default=' ', null=True),
        ),
    ]