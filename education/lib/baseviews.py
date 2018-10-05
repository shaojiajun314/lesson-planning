from json import loads

from rest_framework.views import APIView

class BaseApiView(APIView):
    def err_response(self, form):
        res = {}
        errs = loads(form.errors.as_json())
        desc, code = [], []
        for k, err in errs.items():
            desc.append(err[0]['message'])
            code.append(err[0]['code'])
        res['msg'] = 'fail'
        res['desc'] = desc
        res['code'] = code
        return res
