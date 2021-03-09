import logging
from django.http import HttpResponse
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

    @property
    def delete_url(self):
        return None

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
