from djinn_news.models.liveblog import LiveBlog, LiveBlogUpdate
from djinn_news.models.news import News
from haystack import indexes
from pgsearch.base import ContentSearchIndex


class NewsIndex(ContentSearchIndex, indexes.Indexable):

    published = indexes.DateTimeField(model_attr='publish_from', null=True)

    homepage_published = indexes.DateTimeField(null=True)

    def prepare_homepage_published(self, obj):
        return obj.highlight_from

    def prepare_published(self, obj):
        return obj.date

    def get_model(self):

        return News


class LiveBlogIndex(ContentSearchIndex, indexes.Indexable):

    published = indexes.DateTimeField(model_attr='publish_from', null=True)

    # homepage_published = indexes.DateTimeField(null=True)
    #
    # def prepare_homepage_published(self, obj):
    #     # TODO: MJB
    #     return obj.highlight_from

    def prepare_published(self, obj):
        # TODO: MJB
        return obj.publish_from

    def get_model(self):

        return LiveBlog


class LiveBlogUpdateIndex(ContentSearchIndex, indexes.Indexable):

    published = indexes.DateTimeField(model_attr='publish_from', null=True)

    # homepage_published = indexes.DateTimeField(null=True)

    # def prepare_homepage_published(self, obj):
    #     # TODO: MJB
    #     return obj.highlight_from

    def prepare_published(self, obj):
        return obj.publish_from

    def get_model(self):

        return LiveBlogUpdate
