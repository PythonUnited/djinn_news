from djinn_news.models.news import News
from haystack import indexes
from pgsearch.base import ContentSearchIndex


class NewsIndex(ContentSearchIndex, indexes.Indexable):

    published = indexes.DateTimeField(model_attr='publish_from', null=True)

    def prepare_published(self, obj):
        return obj.date

    def get_model(self):

        return News

    def index_queryset(self, using=None):

        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(is_tmp=False)
