# Generated by Django 3.0.5 on 2021-01-19 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0056_auto_20210119_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthyear',
            field=models.CharField(blank=True, default='2008', max_length=128, null=True),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_image', models.ImageField(blank=True, default='C:\\django_project\\django_project\\media\\uploads\\saramara_defaults.jpg', null=True, upload_to='uploads/')),
                ('post', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Post')),
            ],
        ),
    ]
