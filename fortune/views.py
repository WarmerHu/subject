from django.shortcuts import  render_to_response
from django.http.response import HttpResponse
from django.template.context import RequestContext
import json
from login.dao import select_fortune, select_Cuser

def into_fortune(req):
    return render_to_response('fortune.html',RequestContext(req))

def get_fortune(req):
    p = int(req.GET.get('p'))
    cur = p
    rs = {}
    if p==0:
        cur = 1
        cn = select_Cuser()
        rs['numT'] = cn
    ts = select_fortune(cur)
    rs['fortune'] = ts
    return HttpResponse(json.dumps(rs),content_type="application/json")