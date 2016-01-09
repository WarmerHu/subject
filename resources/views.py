from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http.response import HttpResponse
import json
from resources.dao import select_resources

def into_resources(req):
    return render_to_response('resources.html',RequestContext(req))

def get_resources(req):
    return HttpResponse(json.dumps(select_resources()),content_type="application/json")