from .items import *
from .professions import *
from .races import *
from .skills import *
from .spells import *


def index(request):
    if request.user.is_authenticated:
        return render(request, 'dictionary_base.html', {'menu_attrs': MenuWrapper()})
    else:
        return render(request, 'base.html', {'menu_attrs': MenuWrapper()})
