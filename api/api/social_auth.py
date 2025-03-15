from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from api import models

class PopulateUser(DefaultSocialAccountAdapter):

  def save_user(self, request, sociallogin, form=None):
    super().save_user(request, sociallogin, form=form)
    models.VotingUser.objects.get_or_create(user=sociallogin.user)
