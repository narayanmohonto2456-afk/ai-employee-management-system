from django.utils.cache import add_never_cache_headers


class NoCacheAuthenticatedMiddleware:
    """
    Prevent authenticated pages from being cached by the browser.

    This helps prevent sensitive EMS pages from appearing when
    the user presses the browser Back button after logout.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if request.user.is_authenticated:
            add_never_cache_headers(response)

        return response