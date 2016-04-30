from django.http.response import HttpResponse
import json
from activity.dao import select_activity

def get_activity(req,param):
    return HttpResponse(json.dumps(select_activity(int(param))),content_type="application/json")
