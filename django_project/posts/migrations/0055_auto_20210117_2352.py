# Generated by Django 3.0.5 on 2021-01-17 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0054_auto_20210117_2352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='profile_image',
        ),
        migrations.AddField(
            model_name='post',
            name='item_image',
            field=models.ImageField(blank=True, default='C:\\django_project\\django_project\\media\\profile_image\\saramara_defaults.jpg', null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birthyear',
            field=models.CharField(blank=True, default='1963', max_length=128, null=True),
        ),
    ]