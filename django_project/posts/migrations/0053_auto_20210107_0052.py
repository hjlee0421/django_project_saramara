# Generated by Django 3.0.5 on 2021-01-07 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0052_auto_20210107_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthyear',
            field=models.CharField(blank=True, default='1994', max_length=128, null=True),
        ),
    ]
