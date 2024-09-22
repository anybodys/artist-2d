from django.http import HttpResponse
from django.utils import timezone

from api import models
from painter import generation


def health(request):
  return HttpResponse("OK")


def crontime(request):
  # TODO(kmd): async
  max_gen = models.Generation.objects.order_by('-id').first()
  if not max_gen:
    generation.bootstrap()
  # TODO(kmd): Check if we have enough votes to start a new generation.
  # If so, create the new generation.
  return HttpResponse("OK")
