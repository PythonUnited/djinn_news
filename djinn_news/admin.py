from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .models.liveblog import LiveBlog, LiveBlogUpdate
from .models.news import News


class NewsAdmin(ImageCroppingMixin, admin.ModelAdmin):
    # eigenaar, publicatie datum en de publiceren tot datum
    filter_horizontal = ['images']
    list_display = ('title', 'changed', 'changed_by', 'get_owner', 'publish_from',
                    'publish_to', 'is_global', 'is_sticky', 'publish_for_feed')
    list_filter = ['publish_from', 'is_global', 'publish_for_feed', 'category']
    # raw_id_fields = ['creator', 'changed_by', 'parentusergroup', 'home_image']
    raw_id_fields = ['creator', 'changed_by', 'parentusergroup']
    search_fields = ['title', 'changed_by__userprofile__name', 'text']

    readonly_fields = ['highlight_from']

admin.site.register(News, NewsAdmin)



class LiveBlogUpdateInline(admin.TabularInline):
    model = LiveBlogUpdate
    raw_id_fields = ['changed_by', 'creator']


class LiveBlogAdmin(ImageCroppingMixin, admin.ModelAdmin):

    list_display = ('title', 'changed', 'changed_by', 'get_owner', 'publish_from',
                    'publish_to', 'publish_for_feed', 'is_tmp')
    list_filter = ['publish_from', 'is_global', 'publish_for_feed', 'is_tmp']
    raw_id_fields = ['creator', 'changed_by', 'parentusergroup', 'home_image']
    search_fields = ['title', 'changed_by__userprofile__name', 'text']
    inlines = [LiveBlogUpdateInline]


admin.site.register(LiveBlog, LiveBlogAdmin)


class LiveBlogUpdateAdmin(admin.ModelAdmin):
    list_display = ['liveblog', 'title']
    search_fields = ['title', 'liveblog__title', 'liveblog__changed_by__userprofile__name', 'text']
    raw_id_fields = ['changed_by', 'creator']

admin.site.register(LiveBlogUpdate, LiveBlogUpdateAdmin)
