# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse

from .tasks import hello_world

global r
r = None

def index(request):
    global r
    print dir(r)
    if r:
        print r.result

    r = hello_world.delay(a=1)
    print dir(r)
    # add.AsyncResult()
    # add.apply_async((a, b), queue='laplace')


    return HttpResponse(r)
    # return HttpResponse(u"Fuck the GFW!")
