from django.conf import settings

DEFAULT_DATETIME_INPUT_FORMAT = getattr(
    settings, 'DEFAULT_DATETIME_INPUT_FORMAT', '%d/%m/%Y %H:%M')

DEFAULT_DATE_INPUT_FORMAT = getattr(
    settings, 'DEFAULT_DATE_INPUT_FORMAT', '%d/%m/%Y')

DEFAULT_NEWS_IMAGE_URL = getattr(
    settings, 'DEFAULT_NEWS_IMAGE_URL', '/')

ALLOW_ADD_DOCUMENT_RELATION = getattr(
    settings, 'ALLOW_ADD_DOCUMENT_RELATION', False)
