import datetime

from base.models.ifuser import IFUser


class BackgroundMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        hour = datetime.datetime.today().hour
        img = "bg-image-5"
        if hour < 5:
            img = "bg-image-1"
        elif hour < 10:
            img = "bg-image-2"
        elif hour < 15:
            img = "bg-image-3"
        elif hour < 20:
            img = "bg-image-4"

        request.background_image = img

        # Code to be executed for each request/response after
        # the view is called.

        return self.get_response(request)


class CharacterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        user = request.user

        request.character = None
        if isinstance(user, IFUser):
            request.character = user.active_char

        return self.get_response(request)
