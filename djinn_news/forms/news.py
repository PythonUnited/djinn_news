from django import forms
from django.utils.translation import ugettext_lazy as _
from djinn_forms.widgets.attachment import AttachmentWidget
from djinn_forms.fields.relate import RelateField
from djinn_forms.forms.relate import RelateMixin
from djinn_forms.forms.richtext import RichTextMixin
from djinn_forms.widgets.relate import RelateWidget
from djinn_forms.widgets.richtext import RichTextWidget
from djinn_contenttypes.forms.base import BaseContentForm
from djinn_contenttypes.models.attachment import ImgAttachment
from djinn_news.models import News


class NewsForm(BaseContentForm, RelateMixin, RichTextMixin):

    # Translators: news general help
    help = _("Add a news item. The item will be submitted for publishing")

    title = forms.CharField(label=_("Title"),
                            max_length=100,
                            widget=forms.TextInput())

    text = forms.CharField(
        # Translators: news text label
        label=_("News text"),
        required=True,
        widget=RichTextWidget(
            img_type="djinn_contenttypes.ImgAttachment",
            attrs={'class': 'extended'}
        ))

    is_global = forms.BooleanField(
        # Translators: news is_global label
        label=_("Is global"),
        required=False
        )

    documents = RelateField(
        "related_document",
        ["pgcontent.document"],
        # Translators: news documents label
        label=_("Related documents"),
        required=False,
        # Translators: news documents help
        help_text=_("Select document(s)"),
        widget=RelateWidget(
            attrs={'hint': _("Search document"),
                   # Translators: djinn_news documents link label
                   'label': _("Search documents"),
                   'searchfield': 'title_auto',
                   'template_name': 'search/relate_search_widget.html',
                   'search_url': '/zoeken/zoekajaxlinkdocument/',
                   'ct_searchfield': 'meta_type', },
            # TODO:reverse('haystack_link_popup') is mooier
            )
        )

    images = forms.ModelMultipleChoiceField(
        queryset=ImgAttachment.objects.all(),
        # Translators: news images label
        label=_("Images"),
        required=False,
        widget=AttachmentWidget(
            ImgAttachment,
            "djinn_forms/snippets/imageattachmentwidget.html",
            attrs={"multiple": True}
            ))

    def __init__(self, *args, **kwargs):

        super(NewsForm, self).__init__(*args, **kwargs)

        if not self.instance.get_owner():
            self.fields['owner'].initial = self.user.profile
            self.fields['owner'].widget.initial = True
        self.fields['show_images'].label = _("Show images")
        self.fields['comments_enabled'].label = _("Comments enabled")

        if not self.user.has_perm("djinn_news.manage_news", obj=self.instance):
            del self.fields['is_global']

        self.init_relation_fields()
        self.init_richtext_widgets()

    def save(self, commit=True):

        res = super(NewsForm, self).save(commit=commit)

        self.save_relations(commit=commit)

        return res

    class Meta(BaseContentForm.Meta):
        model = News
        fields = ('title', 'text', 'documents', 'images', 'parentusergroup',
                  'comments_enabled', 'owner', 'publish_from',
                  'publish_to', 'show_images', 'is_global')
