# Generated by Django 3.0.5 on 2021-01-17 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0053_auto_20210107_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='profile_image',
            field=models.ImageField(blank=True, default='C:\\django_project\\django_project\\media\\profile_image\\saramara_defaults.jpg', null=True, upload_to='profile_image'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birthyear',
            field=models.CharField(blank=True, default='1953', max_length=128, null=True),
        ),
    ]
