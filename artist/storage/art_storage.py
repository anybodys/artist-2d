import os

from google.cloud import storage


BUCKET_NAME = f'{os.environ["GOOGLE_CLOUD_PROJECT"]}.appspot.com'

class ArtStorage:

  def __init__(self, generation):
    self.generation = generation
    self.gs = storage.Client()

  def upload_blob(self, source_filepath):
    """Uploads a file to the bucket."""

    filename = os.path.basename(source_filepath)

    bucket = self.gs.bucket(BUCKET_NAME)
    blob = bucket.blob(f'gen-{self.generation}/{filename}')

    blob.upload_from_filename(source_filepath)
