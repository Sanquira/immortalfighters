from .items import *
from .mobs import *
from .skills import *
from .spells import *


@login_required
def index(request):
    return render(request, 'dictionary_base.html')
