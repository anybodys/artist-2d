from django.http import HttpResponse, JsonResponse

from api import art_storage
from api import models


def health(request):
  return HttpResponse("OK")


# TODO: Make this a View class and save ArtStorage on the class.
def art(request):
  gen = int(request.GET.get('gen', -1))
  if gen < 0:
    gen = models.get_current_generation()

  # Return a list of all the requested generation's art metadata.
  return JsonResponse(art_storage.ArtStorage().get_art(gen))
