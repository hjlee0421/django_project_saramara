# Generated by Django 3.0.8 on 2020-09-15 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20200830_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='link',
            field=models.CharField(blank=True, default='NA', max_length=128, null=True),
        ),
    ]