# Generated by Django 3.0.5 on 2020-12-05 07:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0023_remove_user_profile_nickname'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=datetime.datetime(2020, 12, 5, 7, 32, 34, 625248, tzinfo=utc), null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Post')),
            ],
        ),
    ]
