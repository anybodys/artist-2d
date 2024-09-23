import os
import re

from google.cloud import storage


BUCKET_NAME = f'{os.environ["GOOGLE_CLOUD_PROJECT"]}.appspot.com'

BLOB_ID_PATTERN = re.compile(r'gen-(?P<gen>[0-9]+)/(?P<artist_id>.*)\.jpg')


class ArtStorage:

  def __new__(cls):
    """Create or return the singleton instance of the ArtStorage."""
    if not hasattr(cls, 'instance'):
      cls.instance = super(ArtStorage, cls).__new__(cls)
    return cls.instance

  def __init__(self):
    self.gs = storage.Client()
    self.bucket = self.gs.bucket(BUCKET_NAME)

  def get_art(self, generation):
    """Gets the public information about a genearation of art."""
    art = []
    for b in self.bucket.list_blobs(prefix=f'gen-{generation}/'):
      m = BLOB_ID_PATTERN.match(b.name)
      art.append({
        'public_link': b.public_url,
        'generation': m['gen'],
        'artist_id': m['artist_id'],
      })
    return {'art': art}

  def new_image_file(self, generation: int, artist_id: int):
    blob = self.bucket.blob(f'gen-{generation}/{artist_id}.jpg')
    #blob.acl.all().grant_read()
    return blob

  def open(self, blob):
    """Gets the context manager for a filepointer to write the art to."""
    return blob.open(mode='wb', ignore_flush=True)
