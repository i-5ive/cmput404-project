from django.http import HttpResponse


def get_indexjs(request):
    with open('static/index_bundle.js', "rb") as f:
        return HttpResponse(content=f.read(), content_type='text/javascript')
