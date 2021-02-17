from django.urls import reverse

from djinn_contenttypes.views.base import CreateView, UpdateView


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
