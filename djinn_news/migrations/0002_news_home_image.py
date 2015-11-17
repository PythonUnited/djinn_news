# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djinn_contenttypes', '__first__'),
        ('djinn_news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='home_image',
            field=models.ForeignKey(related_name='news_home_image', blank=True, to='djinn_contenttypes.ImgAttachment', null=True),
        ),
    ]
