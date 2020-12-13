# Generated by Django 3.0.5 on 2020-12-12 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0028_auto_20201213_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthyear',
            field=models.CharField(blank=True, default='1972', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='django_project\\media\\profile_image\\saramara_default.jpg', null=True, upload_to='profile_image'),
        ),
    ]
