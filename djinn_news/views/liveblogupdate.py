import logging
from django.urls import reverse
from djinn_contenttypes.views.base import CreateView, UpdateView, DetailView
from djinn_news.models import LiveBlog

log = logging.getLogger(__name__)


class LiveBlogUpdateCreateView(CreateView):

    def get_success_url(self):
        return reverse("djinn_news_view_liveblog", args=[self.object.liveblog_id, self.object.liveblog.slug])


class LiveBlogUpdateUpdateView(UpdateView):

    @property
    def view_url(self):
        return self.get_success_url()

    def get_success_url(self):
        return reverse("djinn_news_view_liveblog", args=[self.object.liveblog_id, self.object.liveblog.slug])


class LiveBlogUpdateCountAjax(DetailView):

    model = LiveBlog
    template_name = "djinn_news/snippets/liveblogupdatecount.html"

    def get_context_data(self, **kwargs):
        '''
        pk is ID of the LiveBlog

        TODO: cache the result of the query, so the database is not hit by every user.

        '''
        ctx = super().get_context_data(**kwargs)

        newerthan_ts = self.request.GET.get('newerthan_ts', None)

        updates_qs = self.object.liveblogupdates.filter(created__gt=newerthan_ts)
        new_updates_count = updates_qs.count()
        # print(f"new updates: {new_updates_count}")

        ctx.update({
            "new_updates_count": new_updates_count,
        })

        return ctx


class LiveBlogUpdateLoadMoreAjax(DetailView):

    model = LiveBlog
    template_name = "djinn_news/snippets/liveblogupdateloadmore.html"

    def get_context_data(self, **kwargs):
        '''
        pk is ID of the LiveBlog

        haalt alle updates van deze liveblog op, vanaf een gegeven timestamp;
        de meest recente bovenaan.
        De slicing en beslissing of 'laad meer' button getoond moet worden gebeurt
        in de template, omdat die ook gebruikt wordt voor het initieel laden
        van de liveblog-detail-pagina.
        '''
        ctx = super().get_context_data(**kwargs)

        olderthan_ts = self.request.GET.get('olderthan_ts', None)

        liveblogupdates_qs = self.object.liveblogupdates.filter(created__lt=olderthan_ts)
        # print(f"new updates: {new_updates_count}")

        ctx.update({
            "liveblogupdates_qs": liveblogupdates_qs.all()
        })

        return ctx
