# Generated by Django 3.0.8 on 2020-08-23 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='post',
            name='mara',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='sara',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(choices=[('사라', '사라'), ('마라', '마라')], default='사라', max_length=128),
        ),
    ]