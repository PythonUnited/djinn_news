from datetime import datetime, timedelta
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from djinn_contenttypes.models import Category

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
from djinn_contenttypes.models.highlight import Highlight
from djinn_news.models import News
from djinn_news import settings as news_settings


class NewsForm(DjinnCroppingMixin, BaseContentForm, RelateMixin, RichTextMixin):

    cropping_field_name = 'image_feed'

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
            attrs={'class': 'extended description_feed_src', 'name': 'text'}
        ))

    documents = RelateField(
        "related_document",
        ["pgcontent.document"],
        # Translators: news documents label
        label=_("Related documents"),
        required=False,
        # Translators: news documents help
        help_text=_("Select document(s)"),
        widget=RelateWidget(
            attrs={
                'hint': _("Search document"),
                # Translators: djinn_news documents link label
                'label': _("Search documents"),
                'searchfield': 'title_auto',
                'template_name':
                'djinn_forms/snippets/relatesearchwidget.html',
                'search_url': '/document_search/',
                'ct_searchfield': 'meta_type',
                'allow_add_relation': news_settings.ALLOW_ADD_DOCUMENT_RELATION,
                'add_relation_url': '/content/add_ajax/document/',
                'add_relation_label': _("Add document")
                },
            )
        )

    images = forms.ModelMultipleChoiceField(
        queryset=ImgAttachment.objects.all(),
        # Translators: news images label
        label=_("Images"),
        required=False,
        widget=AttachmentWidget(
            ImgAttachment,
            "gronet_v3/djinn_forms/snippets/imageattachmentwidget.html",
            attrs={"multiple": True, "show_progress": True, 'inline_edit_enabled': settings.INLINE_EDIT_ENABLED}
            ))

    home_image = ImageField(
        model=ImgAttachment,
        # Translators: Homepage news image label
        label=_("Add homepage image"),
        required=False,
        widget=ImageWidget(
            attrs={
                'size': 'upload_widget_feed',
                'attachment_type': 'djinn_contenttypes.ImgAttachment',
                }
        )
    )
    # Zo zou de widget gelijk zijn aan image toevoegen aan timelinebericht
    # home_image = forms.ModelChoiceField(
    #     queryset=ImgAttachment.objects.all(),
    #     # Translators: Homepage news image label
    #     label=_("Add homepage image"),
    #     required=False,
    #     widget = AttachmentWidget(
    #         ImgAttachment,
    #         "gronet_v3/djinn_forms/snippets/imageattachmentwidget.html",
    #         attrs={"multiple": False, "show_progress": True,
    #                'inline_edit_enabled': settings.INLINE_EDIT_ENABLED}
    #     )
    # )

    image_feed = ImageField(
        model=ImgAttachment,
        # Translators: Homepage rss-feed image label
        label=_("Add rss-feed image"),
        required=False,
        widget=ImageWidget(
            attrs={
                'size': 'news_home_list',
                'attachment_type': 'djinn_contenttypes.ImgAttachment',
                }
        )
    )
    # Zo zou de widget gelijk zijn aan image toevoegen aan timelinebericht
    # image_feed = forms.ModelChoiceField(
    #     queryset=ImgAttachment.objects.all(),
    #     # Translators: Homepage rss-feed image label
    #     label=_("Add rss-feed image"),
    #     required=False,
    #     widget = AttachmentWidget(
    #         ImgAttachment,
    #         "gronet_v3/djinn_forms/snippets/imageattachmentwidget.html",
    #         attrs={"multiple": False, "show_progress": True,
    #                'inline_edit_enabled': settings.INLINE_EDIT_ENABLED}
    #     )
    # )

    highlight_from = forms.DateTimeField(
        # Translators: contenttypes highlight_from label
        label=_("Highlight from"),
        # Translators: contenttypes publish_from help
        help_text=_("Enter a publish-from date and time"),
        required=False,
        widget=DateTimeWidget(
            attrs={'date_hint': _("Date"),
                   'time_hint': _("Time"),
                   'date_format': news_settings.DEFAULT_DATE_INPUT_FORMAT}
            )
        )

    event_dt = forms.DateTimeField(
        # Translators: News event_dt label
        label=_("Event date/time"),
        # Translators: News event_dt help
        help_text=_("Enter the date/time of the associated event"),
        required=False,
        widget=DateTimeWidget(
            attrs={'date_hint': _("Date"),
                   'time_hint': _("Time"),
                   'date_format': news_settings.DEFAULT_DATE_INPUT_FORMAT}
            )
        )

    def __init__(self, *args, **kwargs):

        super(NewsForm, self).__init__(*args, **kwargs)

        if self.instance.is_tmp:
            if not self.instance.publish_to:
                self['publish_to'].initial = datetime.now() + timedelta(days=365)
        if 'category_slug' in self.initial:
            initial_category = Category.objects.filter(slug=self.initial['category_slug']).first()
            self.initial.update({'category': initial_category.id})
        self.fields['show_images'].label = _("Show images")
        self.fields['comments_enabled'].label = _("Comments enabled")
        self.fields['is_sticky'].label = _("Important homepage item")
        self.fields['description_feed'].widget.attrs.update(
            {'data-maxchars': DESCR_FEED_MAX_LENGTH, 'class': 'full count_characters high'})

        if self.initial.get('category_slug') == News.CATEGORY_OCCURRENCE or \
                (self.instance.category_id and self.instance.category.slug == News.CATEGORY_OCCURRENCE):
            # del self.fields['home_image']
            del self.fields['is_sticky']
        else:
            del self.fields['event_dt']

        if not self.user.has_perm("djinn_news.manage_news", obj=self.instance):
            del self.fields['highlight_from']
            del self.fields['category']
            # zijn misschien al verwijderd:
            if 'home_image' in self.fields:
                del self.fields['home_image']
            if 'is_sticky' in self.fields:
                del self.fields['is_sticky']
        else:
            self.fields[
                'highlight_from'].initial = self.instance.highlight_from

        self.init_richtext_widgets()

    def save(self, commit=True):

        object_ct = ContentType.objects.get_for_model(self.instance)

        if commit:
            if self.cleaned_data.get("highlight_from"):
                hlight, created = Highlight.objects.get_or_create(
                    object_id=self.instance.id,
                    object_ct=object_ct)

                hlight.date_from = self.cleaned_data.get("highlight_from")
                hlight.save()

                # del self.cleaned_data['highlight_from']

            # deleten doen we niet meer, want dan is de oorspronkelijke
            # highlight datum weg.
            # Zie http://support.pythonunited.com/view_issue/638
            # als highlight is leeg dan doe wel delete, mits gebruiker permissie heeft
            elif self.user.has_perm("djinn_news.manage_news", obj=self.instance):
                if 'highlight_from' in self.fields.keys() and \
                        self.fields['highlight_from'].empty_values:
                    Highlight.objects.filter(
                        object_id=self.instance.id,
                        object_ct=object_ct).delete()

        res = super(NewsForm, self).save(commit=commit)

        self.save_relations(commit=commit)

        return res

    class Meta(BaseContentForm.Meta):
        model = News
        fields = ('title', 'text', 'event_dt', 'documents', 'images', 'home_image',
                  'parentusergroup', 'comments_enabled', 'owner',
                  'publish_from', 'remove_after_publish_to',
                  'publish_to', 'highlight_from', 'is_sticky',
                  'show_images', 'userkeywords', 'state', 'use_default_image',
                  'publish_for_feed', 'description_feed', 'image_feed',
                  'image_feed_crop',
                  'category',
                  )
