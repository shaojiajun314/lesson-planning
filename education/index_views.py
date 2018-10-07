from django.shortcuts import redirect

from rest_framework.views import APIView

class IndexRedirctView(APIView):
    def get(self, request, *args, **kw):
        return redirect('/static/catalogue/index.html')
        # if request.user.is_authenticated():
        #     return redirect('/static/catalogue/index.html')
        #
        # return redirect('/static/user/login/login.html')
