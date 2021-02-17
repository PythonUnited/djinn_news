# Generated by Django 2.0.13 on 2019-10-03 10:41

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djinn_news', '0005_news_home_image_feed_crop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='home_image_feed_crop',
            field=image_cropping.fields.ImageRatioField('home_image__image', '800x600', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text="Part of the home-image to use in the rss-feed. Upload or change home_image, click 'save and edit again' and then you can select a region to use in the rss feed.", hide_image_field=False, size_warning=True, verbose_name='Foto uitsnede'),
        ),
    ]
