from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from djinn_contenttypes.forms.crop import DjinnCroppingMixin
from djinn_contenttypes.models.feed import DESCR_FEED_MAX_LENGTH
from djinn_forms.widgets.attachment import AttachmentWidget
from djinn_forms.widgets.image import ImageWidget
from djinn_forms.fields.relate import RelateField
from djinn_forms.fields.image import ImageField
from djinn_forms.forms.relate import RelateMixin
from djinn_forms.forms.richtext import RichTextMixin
from djinn_forms.widgets.relate import RelateWidget
from djinn_forms.widgets.richtext import RichTextWidget
from djinn_forms.widgets.datetimewidget import DateTimeWidget
from djinn_contenttypes.forms.base import BaseContentForm
from djinn_contenttypes.models.attachment import ImgAttachment
from djinn_news import settings
from djinn_news.models import LiveBlog
from djinn_news.models.liveblog import LiveBlogUpdate


class LiveBlogForm(DjinnCroppingMixin, BaseContentForm, RelateMixin, RichTextMixin):

    cropping_field_name = 'image_feed'

    # Translators: liveblog general help
    help = _("Add a liveblog. The item will be submitted for publishing")

    title = forms.CharField(label=_("Title"),
                            max_length=100,
                            widget=forms.TextInput())

    text = forms.CharField(
        # Translators: liveblog text label
        label=_("LiveBlog text"),
        required=True,
        widget=RichTextWidget(
            img_type="djinn_contenttypes.ImgAttachment",
            attrs={'class': 'extended description_feed_src', 'name': 'text'}
        ))

    documents = RelateField(
        "related_document",
        ["pgcontent.document"],
        # Translators: liveblog documents label
        label=_("Related documents"),
        required=False,
        # Translators: liveblog documents help
        help_text=_("Select document(s)"),
        widget=RelateWidget(
            attrs={
                'hint': _("Search document"),
                # Translators: djinn_news liveblog documents link label
                'label': _("Search documents"),
                'searchfield': 'title_auto',
                'template_name':
                'djinn_forms/snippets/relatesearchwidget.html',
                'search_url': '/document_search/',
                'ct_searchfield': 'meta_type',
                'allow_add_relation': settings.ALLOW_ADD_DOCUMENT_RELATION,
                'add_relation_url': '/content/add_ajax/document/',
                'add_relation_label': _("Add document")
                },
            )
        )

    images = forms.ModelMultipleChoiceField(
        queryset=ImgAttachment.objects.all(),
        # Translators: liveblog images label
        label=_("Images"),
        required=False,
        widget=AttachmentWidget(
            ImgAttachment,
            "djinn_forms/snippets/imageattachmentwidget.html",
            attrs={"multiple": True}
            ))

    home_image = ImageField(
        model=ImgAttachment,
        # Translators: Homepage liveblog image label
        label=_("Add homepage image"),
        required=False,
        widget=ImageWidget(
            attrs={
                'size': 'upload_widget_feed',
                'attachment_type': 'djinn_contenttypes.ImgAttachment',
                }
        )
    )

    image_feed = ImageField(
        model=ImgAttachment,
        # Translators: Homepage liveblog image label
        label=_("Add rss-feed image"),
        required=False,
        widget=ImageWidget(
            attrs={
                'size': 'liveblog_home_list',
                'attachment_type': 'djinn_contenttypes.ImgAttachment',
                }
        )
    )

    def __init__(self, *args, **kwargs):

        super(LiveBlogForm, self).__init__(*args, **kwargs)

        self.fields['show_images'].label = _("Show images")
        self.fields['comments_enabled'].label = _("Comments enabled")
        self.fields['is_sticky'].label = _("Important homepage item")
        self.fields['description_feed'].widget.attrs.update(
            {'data-maxchars': DESCR_FEED_MAX_LENGTH, 'class': 'full count_characters high'})

        if not self.user.has_perm("djinn_news.manage_news", obj=self.instance):
            del self.fields['home_image']
            del self.fields['is_sticky']

        self.init_richtext_widgets()

    def save(self, commit=True):

        res = super(LiveBlogForm, self).save(commit=commit)

        self.save_relations(commit=commit)

        return res

    class Meta(BaseContentForm.Meta):
        model = LiveBlog
        fields = ('title', 'text', 'documents', 'images', 'home_image',
                  'parentusergroup', 'comments_enabled', 'owner',
                  'publish_from', 'remove_after_publish_to',
                  'publish_to', 'is_sticky',
                  'show_images', 'userkeywords', 'state', 'use_default_image',
                  'publish_for_feed', 'description_feed', 'image_feed',
                  'image_feed_crop')


class LiveBlogUpdateForm(BaseContentForm, RelateMixin, RichTextMixin):

    # Translators: liveblog general help
    help = _("Add a liveblogUpdate. The item will be submitted for publishing")

    title = forms.CharField(label=_("Title"),
                            max_length=100,
                            widget=forms.TextInput())

    text = forms.CharField(
        # Translators: liveblog text label
        label=_("LiveBlogUpdate text"),
        required=True,
        widget=RichTextWidget(
            img_type="djinn_contenttypes.ImgAttachment",
            attrs={'class': 'extended description_feed_src', 'name': 'text'}
        ))

    images = forms.ModelMultipleChoiceField(
        queryset=ImgAttachment.objects.all(),
        # Translators: liveblog images label
        label=_("Images"),
        required=False,
        widget=AttachmentWidget(
            ImgAttachment,
            "djinn_forms/snippets/imageattachmentwidget.html",
            attrs={"multiple": True}
            ))

    def __init__(self, *args, **kwargs):

        super(LiveBlogUpdateForm, self).__init__(*args, **kwargs)

        self.fields['comments_enabled'].label = _("Comments enabled")

        self.init_richtext_widgets()

    def save(self, commit=True):

        if not self.instance.liveblog_id:
            self.instance.liveblog_id = self.initial.get('liveblog', None)
        res = super(LiveBlogUpdateForm, self).save(commit=commit)

        self.save_relations(commit=commit)

        return res

    class Meta(BaseContentForm.Meta):
        model = LiveBlogUpdate
        fields = ('title', 'text', 'images',
                  # 'documents', 'parentusergroup', 'owner',
                  'comments_enabled',
                  #'publish_from', 'remove_after_publish_to',
                  #'publish_to', 'is_sticky',
                  # 'show_images',
                  'userkeywords', 'state',
                  # 'use_default_image',
                  # 'publish_for_feed', 'description_feed', 'image_feed',
                  # 'image_feed_crop'
                  )
