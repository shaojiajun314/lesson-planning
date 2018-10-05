from django.shortcuts import redirect

from rest_framework.views import APIView

class IndexRedirctView(APIView):
    def get(self, request, *args, **kw):
        return redirect('/static/catalogue/index.html')
