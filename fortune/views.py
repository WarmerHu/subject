from django.shortcuts import  render_to_response
from django.http.response import HttpResponse
from django.template.context import RequestContext
import json
from login.dao import select_fortune

def into_fortune(req):
    return render_to_response('fortune.html',RequestContext(req))

def get_fortune(req):
    return HttpResponse(json.dumps(select_fortune()),content_type="application/json")