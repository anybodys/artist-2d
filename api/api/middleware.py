import json

from django.http import HttpResponseBadRequest


def json_request(get_response):
  def middleware(request):
    if request.method in ('POST', 'PUT') and request.headers['Content-type'] == 'application/json':
      try:
        request.post_json = json.loads(request.body)
      except:
        return HttpResponseBadRequest('Invalid JSON payload')
    return get_response(request)

  return middleware
