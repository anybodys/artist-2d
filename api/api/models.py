from django.db import models


def get_current_generation():
  # Get the max id of where `active_date` is not `Null`.
  gen = (Generation.objects
         .filter(active_date__isnull=False)
         .order_by("-id")
         .values_list("id", flat=True)[0])
  return gen


class DatetimeManager(models.Manager):
  def get_queryset(self):
    return super().get_queryset().filter(deleted_date__isnull=True)

class Datetime(models.Model):
  class Meta:
    abstract = True

  objects = DatetimeManager()

  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)
  deleted_date = models.DateTimeField(null=True)

class Generation(Datetime):
  id = models.AutoField(primary_key=True)
  active_date = models.DateTimeField(null=True)
  inaction_date = models.DateTimeField(null=True)

  def __str__(self):
    return f'{self.id}: {self.active_date} - {self.inaction_date}'
