from django.template import Library
from djinn_contenttypes.registry import CTRegistry

register = Library()


@register.inclusion_tag('djinn_news/snippets/connected_liveblogupdates_list.html',
                        takes_context=True)
def all_liveblogupdates(context, liveblog, title=None, edit=False,
                        number_of_items=10):


    liveblogupdates = liveblog.liveblogupdates.all()

    context.update({'request': context['request'],
                    'title': title,
                    'is_edit': edit,
                    'items': liveblogupdates,
                    'contentitem_name': CTRegistry.get(liveblog.ct_name)['name_plural']})
    return context
