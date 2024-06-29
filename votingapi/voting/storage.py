import os

from flask import g

from voting import requests


# Pull here so we fail early if not defined.
BASE_URL = os.environ['STORAGEAPI_URL']


def get_api():
  if 'storageapi' not in g:
    g.storageapi = StorageApi()
  return g.storageapi


class StorageApi:

  def __init__(self):
    self.session = requests.Session(BASE_URL)

  def get_art(self, generation):
    return self.session.get('art', params={'gen': generation})
