# Generated by Django 3.0.5 on 2021-01-23 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0061_auto_20210122_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthyear',
            field=models.CharField(blank=True, default='1986', max_length=128, null=True),
        ),
    ]
