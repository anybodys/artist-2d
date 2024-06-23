import os

from flask import current_app, g
import requests


# Pull here so we fail early if not defined.
BASE_URL = os.environ['STORAGEAPI_URL']


def get_api():
  if 'storageapi' not in g:
    g.storageapi = StorageApi()
  return g.storageapi


class StorageApi:

  def __init__(self):
    self.session = requests.Session()

  def get_art(self, generation):
    response = self.session.get(f'{BASE_URL}/api/art', params={'gen': generation})
    return response.json()
