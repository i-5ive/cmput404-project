from django.http import HttpResponse
from django.views.decorators.cache import cache_page


@cache_page(300)
def get_indexjs(request):
    with open('static/index_bundle.js', "rb") as f:
        return HttpResponse(content=f.read(), content_type='text/javascript')
