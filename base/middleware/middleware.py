import datetime

from base.models import IFUser
from base.models.character import Character
from dictionary.models.profession import BaseProfession
from dictionary.models.race import Race


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


class StatisticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        statistics = {
            'race': list(),
            'profession': list(),
            'registered': IFUser.objects.count(),
            'online': IFUser.objects.filter(is_active=True).count()
        }

        for race in Race.objects.all():
            statistics['race'].append((race.name, Character.objects.filter(race=race).count()))
        for profession in BaseProfession.objects.filter(parentProf=None):
            statistics['profession'].append((profession.name, Character.objects.filter(profession=profession).count()))

        request.statistics = statistics

        return self.get_response(request)
