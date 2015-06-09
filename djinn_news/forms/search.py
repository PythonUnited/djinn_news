from datetime import datetime
from djinn_search.forms.base import SearchForm


class HomepageNewsSearchForm(SearchForm):

    spelling_query = None

    def extra_filters(self, skip_filters=None):

        super(HomepageNewsSearchForm, self).extra_filters(
            skip_filters=skip_filters)

        self.sqs = self.sqs.filter(homepage_published__lte=datetime.now())
