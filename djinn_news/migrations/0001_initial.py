# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pgauth.base
import djinn_contenttypes.models.sharing
import djinn_contenttypes.models.publishable
import django.db.models.deletion
from django.conf import settings
import djinn_likes.models.likeable
import djinn_contenttypes.models.relatable


class Migration(migrations.Migration):

    dependencies = [
        ('djinn_contenttypes', '__first__'),
        ('pgauth', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('changed', models.DateTimeField(auto_now=True, verbose_name='Changed')),
                ('removed_creator_name', models.CharField(max_length=100, null=True, verbose_name='Creator naam', blank=True)),
                ('userkeywords', models.CharField(max_length=500, null=True, verbose_name='Keywords', blank=True)),
                ('is_tmp', models.BooleanField(default=False, verbose_name='Temporary')),
                ('publish_from', models.DateTimeField(default=None, null=True, verbose_name='Publish from', db_index=True, blank=True)),
                ('publish_to', models.DateTimeField(default=None, null=True, verbose_name='Publish to', db_index=True, blank=True)),
                ('publish_notified', models.BooleanField(default=False, help_text='Publish event is sent', verbose_name='Event sent')),
                ('unpublish_notified', models.BooleanField(default=False, help_text='Un-publish event is sent', verbose_name='Event sent')),
                ('remove_after_publish_to', models.BooleanField(default=False, verbose_name='Remove the content ater publication to has past')),
                ('comments_enabled', models.BooleanField(default=1, verbose_name="Collega's kunnen reageren")),
                ('text', models.TextField(null=True, blank=True)),
                ('show_images', models.BooleanField(default=True)),
                ('is_global', models.BooleanField(default=False)),
                ('changed_by', models.ForeignKey(related_name='news_changed_by', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(related_name='news_creator', to=settings.AUTH_USER_MODEL)),
                ('images', models.ManyToManyField(to='djinn_contenttypes.ImgAttachment')),
                ('parentusergroup', models.ForeignKey(related_name='news_parentusergroup', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='pgauth.UserGroup', null=True)),
            ],
            bases=(djinn_contenttypes.models.publishable.PublishableMixin, models.Model, pgauth.base.LocalRoleMixin, djinn_contenttypes.models.sharing.SharingMixin, djinn_contenttypes.models.relatable.RelatableMixin, djinn_likes.models.likeable.LikeableMixin),
        ),
    ]
