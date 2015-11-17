# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djinn_news', '0002_news_home_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='is_sticky',
            field=models.BooleanField(default=False),
        ),
    ]
