# Generated by Django 3.0.5 on 2020-12-26 09:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0039_auto_20201218_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='mara_users',
            field=models.ManyToManyField(related_name='mara_Voter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='sara_users',
            field=models.ManyToManyField(related_name='sara_voter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='birthyear',
            field=models.CharField(blank=True, default='1978', max_length=128, null=True),
        ),
    ]