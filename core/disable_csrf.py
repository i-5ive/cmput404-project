from django.utils.deprecation import MiddlewareMixin

# TODO: put this in external code documentation
# Credit to Venkatesh Mondi at https://stackoverflow.com/a/33778953
class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)