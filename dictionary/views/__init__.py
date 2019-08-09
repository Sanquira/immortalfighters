from django.contrib.auth.decorators import login_required

from .items import *
from .professions import *
from .races import *
from .skills import *
from .spells import *


@login_required
def index(request):
    return render(request, 'dictionary_base.html')
