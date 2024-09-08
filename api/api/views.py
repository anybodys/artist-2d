from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from api import art_storage
from api import models


def health(request):
  return HttpResponse("OK")


# TODO: Make this a View class and save ArtStorage on the class.
def art(request):
  gen = int(request.GET.get('gen', 0))
  if gen < 0:
    gen = models.get_current_generation()

  # Return a list of all the requested generation's art metadata.
  return JsonResponse(art_storage.ArtStorage().get_art(gen))


def me(request):
  ret = {}
  if request.user.is_authenticated:
    ret.update({
      'username': request.user.get_username(),
      'name': request.user.first_name,
      'email': request.user.email,
    })
  return JsonResponse(ret)


@login_required
def vote(request):
  art_id = request.POST['art']
  new_vote = models.Vote.objects.create(
    user=request.user.votinguser,
    art_id=art_id,
  )
  return JsonResponse({})
