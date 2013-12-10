from django.contrib.contenttypes.models import ContentType
from django.db.models import signals
from django.contrib.auth.models import Permission
from pgauth.models import Role
from pgauth.settings import USER_ROLE_ID, OWNER_ROLE_ID
from djinn_news import models


def create_permissions(**kwargs):

    contenttype = ContentType.objects.get(
        app_label='djinn_news',
        model='news')

    role_user = Role.objects.get(name=USER_ROLE_ID)
    role_owner = Role.objects.get(name=OWNER_ROLE_ID)

    add, created = Permission.objects.get_or_create(
        codename="add_news",
        content_type=contenttype,
        defaults={'name': 'Add news'})

    edit, created = Permission.objects.get_or_create(
        codename="change_news",
        content_type=contenttype,
        defaults={'name': 'Change news'})

    delete, created = Permission.objects.get_or_create(
        codename="delete_news",
        content_type=contenttype,
        defaults={'name': 'Delete news'})

    role_user.add_permission_if_missing(add)
    role_owner.add_permission_if_missing(edit)
    role_owner.add_permission_if_missing(delete)


signals.post_syncdb.connect(create_permissions, sender=models)
