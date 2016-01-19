from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse
from django.template.context import RequestContext

def into_fortune(req):
    return render_to_response('fortune.html',RequestContext(req))

def get_fortune(req):
    