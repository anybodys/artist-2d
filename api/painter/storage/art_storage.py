""" DEPRECCATED !!! DELETE ME DELETE ME"""

import os

from google.cloud import storage


BUCKET_NAME = f'{os.environ["GOOGLE_CLOUD_PROJECT"]}.appspot.com'

class ArtStorage:

  def __init__(self):
    self.gs = storage.Client()
    self.bucket = self.gs.bucket(BUCKET_NAME)

