# Generated by Django 3.0.5 on 2021-01-01 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0048_auto_20201231_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthyear',
            field=models.CharField(blank=True, default='1960', max_length=128, null=True),
        ),
    ]
