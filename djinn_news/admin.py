from django.contrib import admin
from image_cropping import ImageCroppingMixin
from .models.news import News


class NewsAdmin(ImageCroppingMixin, admin.ModelAdmin):
    # eigenaar, publicatie datum en de publiceren tot datum
    filter_horizontal = ['images']
    list_display = ('title', 'changed_by', 'get_owner', 'publish_from',
                    'publish_to', 'is_global', 'is_sticky', 'publish_for_feed')
    list_filter = ['publish_from', 'is_global', 'publish_for_feed']
    # raw_id_fields = ['creator', 'changed_by', 'parentusergroup', 'home_image']
    raw_id_fields = ['creator', 'changed_by', 'parentusergroup']
    search_fields = ['title', 'changed_by__userprofile__name', 'text']

    readonly_fields = ['highlight_from']

admin.site.register(News, NewsAdmin)
