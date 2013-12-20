from djinn_news.models.news import News
from haystack import indexes
from pgsearch.base import ContentSearchIndex


class NewsIndex(ContentSearchIndex, indexes.Indexable):

    def get_model(self):

        return News
