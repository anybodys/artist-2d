import os

from google.cloud import storage


BUCKET_NAME = f'{os.environ["GOOGLE_CLOUD_PROJECT"]}.appspot.com'

class ArtStorage:

  def __init__(self):
    self.gs = storage.Client()
    self.bucket = self.gs.bucket(BUCKET_NAME)

  def open(self, generation, artist_id):
    """Gets the context manager for a filepointer to write the art to."""
    blob = self.bucket.blob(f'gen-{generation}/{artist_id}.jpg')
    return blob.open(mode='wb', ignore_flush=True)
