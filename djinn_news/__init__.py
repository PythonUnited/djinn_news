
def get_urls():

    from .urls import urlpatterns

    return urlpatterns

def get_js():

    return ["djinn_news.js"]

def get_css():

    return ["djinn_news.css"]
