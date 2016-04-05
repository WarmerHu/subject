from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http.response import HttpResponse
import json
from jobs.dao import select_jobs
from jobs.controller import JobCraw

def into_jobs(req):
    return render_to_response('jobs.html',RequestContext(req))

def get_jobs(req):
    JobCraw()
    return HttpResponse(json.dumps(select_jobs()),content_type="application/json")
