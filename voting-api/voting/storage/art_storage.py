import os
import re

from google.cloud import storage


BUCKET_NAME = f'{os.environ["GOOGLE_CLOUD_PROJECT"]}.appspot.com'

BLOB_ID_PATTERN = re.compile(r'gen-(?P<gen>[0-9]+)/(?P<artist_id>.*)\.jpg')


class ArtStorage:

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
